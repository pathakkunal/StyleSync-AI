import re
import os

def automate_dashboard_setup():
    input_filename = "code.html"
    output_filename = "dashboard.html"

    # 1. Check if the source file exists
    if not os.path.exists(input_filename):
        print(f"❌ Error: '{input_filename}' not found. Please save your Stitch UI code as '{input_filename}' first.")
        return

    print(f"Reading {input_filename}...")
    with open(input_filename, "r", encoding="utf-8") as f:
        html = f.read()

    # --- Step 1: Inject IDs into the HTML elements ---
    
    print("Injecting IDs for interactivity...")

    # Inject ID for the Drop Zone & Hidden Input
    # We look for the dashed border div that acts as the drop zone
    if 'border-dashed' in html:
        html = re.sub(
            r'(<div[^>]*border-dashed[^>]*>)', 
            r'\1\n<input type="file" id="fileInput" class="hidden" accept="image/*" />', 
            html, count=1
        )
        html = html.replace('border-dashed', 'id="dropZone" border-dashed')

    # Inject ID for the "Browse Files" button
    if 'Browse Files' in html:
        html = re.sub(r'(<button[^>]*>)(\s*Browse Files)', r'<button id="browseBtn" \1\2', html)

    # Inject ID for the "Start Agent Workflow" button
    if 'Start Agent Workflow' in html:
        html = re.sub(r'(<button[^>]*bg-gradient-to-r[^>]*>)', r'\1 id="startBtn"', html)
        # Cleanup potential duplicate IDs if run multiple times
        html = html.replace('id="startBtn" id="startBtn"', 'id="startBtn"')

    # Inject ID for the JSON Output block
    if '<code class="language-json">' in html:
        html = html.replace('<code class="language-json">', '<code id="jsonOutput" class="language-json">')

    # --- Step 2: Append the JavaScript Logic ---

    print("Injecting the Brain (JavaScript)...")

    js_logic = """
<script>
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');
    const startBtn = document.getElementById('startBtn');
    const jsonOutput = document.getElementById('jsonOutput');

    // 1. Handle File Selection
    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation(); 
        fileInput.click();
    });

    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            const fileName = fileInput.files[0].name;
            const pText = dropZone.querySelector('p.text-lg') || dropZone.querySelector('p');
            if(pText) pText.textContent = "File Selected: " + fileName;
            dropZone.classList.add('border-emerald-500');
        }
    });

    // 2. The "Start Agent Workflow" Logic
    startBtn.addEventListener('click', async () => {
        if (!fileInput.files.length) {
            alert("Please select an image first!");
            return;
        }

        const originalText = startBtn.innerHTML;
        startBtn.innerHTML = `<span class="text-white font-bold animate-pulse">Running Agents...</span>`;
        startBtn.disabled = true;

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        try {
            const response = await fetch("http://localhost:8000/generate-catalog", {
                method: "POST",
                body: formData
            });

            if (!response.ok) throw new Error("API Error");

            const data = await response.json();
            jsonOutput.innerHTML = syntaxHighlight(data);

        } catch (error) {
            console.error(error);
            jsonOutput.textContent = "Error connecting to backend.\\nMake sure 'python main.py' is running!";
        } finally {
            startBtn.innerHTML = originalText;
            startBtn.disabled = false;
        }
    });

    // Helper: Format JSON with Tailwind Colors
    function syntaxHighlight(json) {
        if (typeof json != 'string') {
            json = JSON.stringify(json, undefined, 2);
        }
        json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        return json.replace(/("(\\\\u[a-zA-Z0-9]{4}|\\\\[^u]|[^\\\\"])*"(\s*:)?|\\b(true|false|null)\\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
            let cls = 'text-purple-400';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 'text-emerald-500';
                } else {
                    cls = 'text-sky-300';
                }
            }
            return '<span class="' + cls + '">' + match + '</span>';
        });
    }
</script>
</body>
"""
    # Replace the closing body tag with our script
    html = html.replace('</body>', js_logic)

    # --- Step 3: Save the Result ---
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Success! Generated '{output_filename}'.")
    print("👉 You can now open 'dashboard.html' in your browser.")

if __name__ == "__main__":
    automate_dashboard_setup()
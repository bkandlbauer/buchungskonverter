const dropZone = document.getElementById("dropZone");
        const fileInput = document.getElementById("fileInput");
        let selectedFile = null;

        dropZone.addEventListener("click", () => fileInput.click());
        dropZone.addEventListener("dragover", (event) => {
            event.preventDefault();
            dropZone.classList.add("highlight");
        });
        dropZone.addEventListener("dragleave", () => dropZone.classList.remove("highlight"));
        dropZone.addEventListener("drop", (event) => {
            event.preventDefault();
            dropZone.classList.remove("highlight");
            
            if (event.dataTransfer.files.length) {
                selectedFile = event.dataTransfer.files[0];
                dropZone.textContent = selectedFile.name;
            }
        });
        fileInput.addEventListener("change", () => {
            if (fileInput.files.length) {
                selectedFile = fileInput.files[0];
                dropZone.textContent = selectedFile.name;
            }
        });

        async function uploadXML(url, company) {
            if (!selectedFile) {
                alert("Bitte zuerst eine Datei auswählen.");
                return;
            }

            const reader = new FileReader();
            reader.onload = async function(event) {
                const xmlContent = event.target.result;

                try {
                    const response = await fetch(url, {
                        method: "POST",
                        headers: { "Content-Type": "application/xml" },
                        body: xmlContent
                    });

                    if (!response.ok) {
                        throw new Error("Server error: " + (await response.text()));
                    }

                    const csvData = await response.text();
                    downloadCSV(csvData, company);
                } catch (error) {
                    console.error("Error:", error);
                    alert("Conversion failed: " + error.message);
                }
            };
            reader.readAsText(selectedFile);
        }

        function downloadCSV(csvContent, company) {
            const blob = new Blob([csvContent], { type: "text/csv" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = company + ".csv";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
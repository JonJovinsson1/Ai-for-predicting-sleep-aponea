document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById("file-upload");
    const fileDrag = document.getElementById("file-drag");
    const uploadForm = document.getElementById("file-upload-form");
    const uploadCardContainer = document.getElementById("upload-card-container");
    const predictionCardContainer = document.getElementById("prediction-card-container");
    const analyseButton = document.getElementById("analyse-button");
    const predictionOutput = document.getElementById("prediction-output");

    // Handle file selection and drag-and-drop events
    if (fileDrag && fileInput) {
        fileDrag.addEventListener("click", function () {
            fileInput.click();
        });
    }

    if (fileInput) {
        fileInput.addEventListener("change", function () {
            const fileName = fileInput.files[0].name;
            document.getElementById("file-upload-text").innerHTML = `<i class="bi bi-file-earmark"></i><p>File selected: ${fileName}</p>`;
        });
    }

    if (uploadForm) {
        uploadForm.addEventListener("submit", function (e) {
            e.preventDefault(); 

            const formData = new FormData(uploadForm);

            fetch("/upload", {
                method: "POST",
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error("Upload failed");
                }
            })
            .then(data => {
                alert("File uploaded successfully!");
                uploadCardContainer.style.display = "none"; 
                predictionCardContainer.style.display = "block"; 
            })
            .catch(error => {
                alert("Error uploading file.");
                console.error(error);
            });
        });
    }

    if (analyseButton) {
        analyseButton.addEventListener("click", function () {
            predictionOutput.innerHTML = "";  // Clear previous output

            fetch("/run-prediction")
            .then(response => response.body.getReader())
            .then(reader => {
                const decoder = new TextDecoder();
                function read() {
                    reader.read().then(({ done, value }) => {
                        if (done) {
                            return;
                        }
                        predictionOutput.innerHTML += decoder.decode(value);  // Append output to the container
                        read();  // Continue reading
                    });
                }
                read();  // Start reading
            })
            .catch(error => {
                predictionOutput.innerHTML = "Error running prediction: " + error;
            });
        });
    }
});

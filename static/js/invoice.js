function askAI() {

    // Get the uploaded file
    let file = document.getElementById("file").files[0];

    if (!file) {
        alert("Please upload an invoice first.");
        return;
    }

    // Prepare form data for upload
    let xhr = new XMLHttpRequest();
    let formData = new FormData();
    formData.append("file", file);

    // Show loading animation and hide previous results
    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("results").classList.add("hidden");
    document.getElementById("heatmap-img").style.display = "none";

    xhr.onreadystatechange = function () {

        if (xhr.readyState === 4) {

            // Hide loading animation
            document.getElementById("loading").classList.add("hidden");

            // Handle server-side error responses
            if (xhr.status !== 200) {
                alert("Server error. Please check backend logs.");
                return;
            }

            // Parse server response
            let data;
            try {
                data = JSON.parse(xhr.responseText);
            } catch (e) {
                alert("Invalid response from server.");
                return;
            }

            // Handle errors returned by backend
            if (!data.success) {
                alert("Error: " + (data.error || "Unknown error occurred"));
                return;
            }

            let r = data.results || {};

            // Update extracted fields and apply confidence styling
            const fields = ['invoice_number', 'date', 'amount', 'vendor', 'tax'];
            fields.forEach(field => {
                const element = document.getElementById(field);

                if (element && r[field]) {
                    const confidence = r[field].confidence;
                    element.innerText = r[field].answer;
                    element.className = getConfidenceClass(confidence);
                }
            });

            // Items may contain multiline text
            if (r.items) {
                document.getElementById('items').innerText = r.items.answer;
            }

            // Display heatmap if available
            const img = document.getElementById("heatmap-img");
            if (data.heatmap) {
                img.src = data.heatmap;
                img.style.display = "block";
            } else {
                img.style.display = "none";
            }

            // Show results section
            document.getElementById("results").classList.remove("hidden");
        }
    };

    // Send request to backend
    xhr.open("POST", "/invoice");
    xhr.send(formData);
}


// Map confidence score to CSS class
function getConfidenceClass(confidence) {
    if (confidence >= 80) return 'high-confidence';
    if (confidence >= 60) return 'good-confidence';
    if (confidence >= 40) return 'medium-confidence';
    if (confidence >= 20) return 'low-confidence';
    return 'very-low-confidence';
}

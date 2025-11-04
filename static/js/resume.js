function askResumeAI() {
    // Get uploaded resume file
    let file = document.getElementById("file").files[0];

    if (!file) {
        alert("Please upload a resume first.");
        return;
    }

    // Prepare request payload
    let xhr = new XMLHttpRequest();
    let form = new FormData();
    form.append("file", file);

    // Show loading and hide previous results
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

            // Parse response safely
            let data;
            try {
                data = JSON.parse(xhr.responseText);
            } catch (e) {
                alert("Invalid response from server.");
                return;
            }

            // Check if backend returned an error
            if (!data.success) {
                alert("Error: " + (data.error || "Unknown error occurred"));
                return;
            }

            let r = data.results || {};

            // Update resume fields safely (avoids undefined values)
            document.getElementById("name").innerText =
                (r.name && r.name.answer) ? r.name.answer : "Not found";

            document.getElementById("email").innerText =
                (r.email && r.email.answer) ? r.email.answer : "Not found";

            document.getElementById("phone").innerText =
                (r.phone && r.phone.answer) ? r.phone.answer : "Not found";

            document.getElementById("skills").innerText =
                (r.skills && r.skills.answer) ? r.skills.answer : "Not found";

            document.getElementById("education").innerText =
                (r.education && r.education.answer) ? r.education.answer : "Not found";

            document.getElementById("experience").innerText =
                (r.experience && r.experience.answer) ? r.experience.answer : "Not found";

            // Show heatmap image if available
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
    xhr.open("POST", "/resume");
    xhr.send(form);
}

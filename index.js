document.addEventListener("DOMContentLoaded", function () {
    const detectButton = document.querySelector("button[type='submit']");
    const descriptionInput = document.getElementById("description");
    const companyInput = document.getElementById("company-name"); // Fixed ID

    detectButton.addEventListener("click", async function (event) {
        event.preventDefault(); // Prevent form submission

        const description = descriptionInput.value.trim();
        const company_name = companyInput.value.trim(); // Get company name

        if (!description) {
            alert("Please enter a job description.");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ description, company_name }), // Send both
            });

            const data = await response.json();

            if (response.ok) {
                alert(`Prediction: ${data.prediction}`);
            } else {
                alert("Error: " + (data.error || "Unknown error occurred"));
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Failed to connect to the server. Make sure the backend is running.");
        }
    });
});

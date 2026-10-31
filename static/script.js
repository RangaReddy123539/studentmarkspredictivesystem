document.getElementById("predictionForm").addEventListener("submit", function(event) {

    event.preventDefault();

    const data = {
        age: document.getElementById("age").value,
        sex: document.getElementById("sex").value,
        studytime: document.getElementById("studytime").value,
        failures: document.getElementById("failures").value,
        absences: document.getElementById("absences").value,
        Medu: document.getElementById("Medu").value,
        Fedu: document.getElementById("Fedu").value,
        goout: document.getElementById("goout").value,
        health: document.getElementById("health").value,
        internet: document.getElementById("internet").value,
        G1: document.getElementById("G1").value,
        G2: document.getElementById("G2").value
    };

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {

        if (result.success) {

            document.getElementById("grade").textContent =
                result.predicted_grade + " / 20";

            document.getElementById("performance").textContent =
                result.performance;

            document.getElementById("risk").textContent =
                result.risk;

        } else {

            alert("Error: " + result.error);

        }

    })
    .catch(error => {

        alert("Unable to connect to the Flask server.");

        console.error(error);

    });

});
const submitBtn = document.getElementById("submitBtn");
const clearBtn = document.getElementById("clearBtn");
const resultDiv = document.getElementById("result");

submitBtn.addEventListener("click", async () => {
    const syllabus = document.getElementById("syllebus").value;
    const studentBio = document.getElementById("student_level").value;
    const language = document.getElementById("language").value;
    const timeLimit = document.getElementById("time").value;

    if (!syllabus || !studentBio || !timeLimit) {
        alert("Please fill all fields");
        return;
    }

    resultDiv.innerText = "Finding best videos...";

    try {
        const response = await fetch("http://127.0.0.1:8000/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                syllabus: syllabus,
                student_bio: studentBio,
                language: language,
                time_limit: timeLimit
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Server error");
        }

        const data = await response.json();
        resultDiv.innerText = data.result;

    } catch (error) {
        resultDiv.innerText = "Error: " + error.message;
    }
});

clearBtn.addEventListener("click", () => {
    document.getElementById("syllebus").value = "";
    document.getElementById("student_level").value = "";
    document.getElementById("time").value = "";
    resultDiv.innerText = "";
}); 

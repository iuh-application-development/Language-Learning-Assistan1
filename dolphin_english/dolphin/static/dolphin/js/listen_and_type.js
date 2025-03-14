document.addEventListener("DOMContentLoaded", function () {
    let exercises = document.querySelectorAll(".exercise-box"); // Lấy danh sách bài tập
    let currentExerciseIndex = 0;
    let totalExercises = exercises.length;

    // ✅ Hiển thị chỉ bài tập đầu tiên
    function updateExerciseDisplay() {
        exercises.forEach((exercise, index) => {
            exercise.style.display = index === currentExerciseIndex ? "block" : "none";
        });

        // ✅ Cập nhật số thứ tự bài tập
        document.querySelectorAll(".exercise-count").forEach((count) => {
            count.textContent = `${currentExerciseIndex + 1} / ${totalExercises}`;
        });

        // ✅ Cập nhật audio khi chuyển bài
        let currentExercise = exercises[currentExerciseIndex];
        let audioElement = currentExercise.querySelector("audio");
        let newAudioSrc = audioElement.querySelector("source").src;

        audioElement.setAttribute("src", newAudioSrc);
        audioElement.load();
    }

    // ✅ Chuyển đến bài tập tiếp theo
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("nextBtn")) {
            if (currentExerciseIndex < totalExercises - 1) {
                currentExerciseIndex++;
                updateExerciseDisplay();
            }
        }
    });

    // ✅ Quay lại bài tập trước
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("preBtn")) {
            if (currentExerciseIndex > 0) {
                currentExerciseIndex--;
                updateExerciseDisplay();
            }
        }
    });

    // ✅ Hàm loại bỏ dấu câu và chuyển về chữ thường
    function cleanText(text) {
        return text
            .toLowerCase() // Chuyển tất cả về chữ thường
            .replace(/[.,!?;:"'()-]/g, "") // Loại bỏ dấu câu
            .replace(/\s+/g, " ") // Chuẩn hóa khoảng trắng (loại bỏ khoảng trắng thừa)
            .trim(); // Xóa khoảng trắng đầu/cuối
    }

    // ✅ Kiểm tra kết quả nhập vào
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("checkBtn")) {
            let currentExercise = exercises[currentExerciseIndex];

            // Lấy đáp án đúng từ `data-correct`
            let correctAnswer = cleanText(currentExercise.dataset.correct);
            let userAnswer = cleanText(currentExercise.querySelector(".userInput").value);

            console.log("User Answer (Cleaned):", userAnswer);
            console.log("Correct Answer (Cleaned):", correctAnswer);

            if (userAnswer === correctAnswer) {
                alert("✅ Correct!");
            } else {
                alert("❌ Try again!");
            }
        }
    });

    // ✅ Bỏ qua bài tập (Xóa input và chuyển sang bài tiếp theo)
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("skipBtn")) {
            let currentExercise = exercises[currentExerciseIndex];
            let userInput = currentExercise.querySelector(".userInput");
            
            if (userInput) {
                userInput.value = ""; // Xóa nội dung nhập vào
            }

            // ✅ Chuyển sang bài tập tiếp theo nếu chưa phải bài cuối cùng
            if (currentExerciseIndex < totalExercises - 1) {
                currentExerciseIndex++;
                updateExerciseDisplay();
            }
        }
    });

    // ✅ Khởi tạo giao diện ban đầu
    updateExerciseDisplay();
});

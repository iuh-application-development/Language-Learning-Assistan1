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
    // ✅ Hàm loại bỏ dấu câu và chuyển về chữ thường
    function cleanText(text) {
        return text
            .toLowerCase() // Chuyển tất cả về chữ thường
            .replace(/[.,!?;:"'()-]/g, "") // Loại bỏ dấu câu
            .replace(/\s+/g, " ") // Chuẩn hóa khoảng trắng (loại bỏ khoảng trắng thừa)
            .trim(); // Xóa khoảng trắng đầu/cuối
    }

    // ✅ Hàm so sánh chính tả và hiển thị từ đúng với dấu '*'
    function checkSpelling(userAnswer, correctAnswer) {
        let result = ''; // Chuỗi kết quả
        let userWords = userAnswer.split(' '); // Tách các từ từ userAnswer
        let correctWords = correctAnswer.split(' '); // Tách các từ từ correctAnswer
    
        // Lặp qua từng từ để so sánh
        for (let i = 0; i < correctWords.length; i++) {
            let userWord = userWords[i] || ''; // Nếu không có từ tương ứng trong userInput, coi như chuỗi rỗng
            let correctWord = correctWords[i];
    
            // So sánh từng ký tự trong từ
            let wordResult = '';
            let minLength = Math.min(userWord.length, correctWord.length);
    
            // So sánh ký tự đúng và hiển thị màu xanh cho ký tự đúng
            for (let j = 0; j < minLength; j++) {
                if (userWord[j] === correctWord[j]) {
                    wordResult += `<span style="color: green; font-size: 20px;">${correctWord[j]}</span>`; // Hiển thị đúng ký tự màu xanh
                } else {
                    wordResult += '*'; // Nếu ký tự sai, thay bằng dấu '*'
                }
            }
    
            // Nếu userWord ngắn hơn correctWord, thêm dấu '*' cho phần còn lại của correctWord
            if (userWord.length < correctWord.length) {
                wordResult += '*'.repeat(correctWord.length - userWord.length);
            }
    
            result += wordResult + ' '; // Nối các từ lại với nhau
        }
    
        return result.trim(); // Trả về kết quả
    }
    
    // Nút next và replay
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("nextBtnHidden")) {
            let currentExercise = event.target.closest(".exercise-box");
            let nextExercise = currentExercise.nextElementSibling;
            if (nextExercise) {
                currentExercise.style.display = "none";
                nextExercise.style.display = "block";
            }
        }
        if (event.target.classList.contains("replayBtn")) {
            let currentExercise = event.target.closest(".exercise-box");
            let audioElement = currentExercise.querySelector("audio");
            audioElement.currentTime = 0;
            audioElement.play();
        }
    });

    // ✅ Kiểm tra kết quả nhập vào
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("checkBtn")) {
            let currentExercise = event.target.closest(".exercise-box");
            let correctAnswer = currentExercise.dataset.correct;
    
            if (!correctAnswer) {
                return; // Nếu không có đáp án đúng, không làm gì cả
            }
    
            correctAnswer = cleanText(correctAnswer);
            let userInputElement = currentExercise.querySelector(".userInput");
    
            if (!userInputElement) {
                return; // Nếu không tìm thấy trường nhập liệu, không làm gì cả
            }
    
            let userAnswer = cleanText(userInputElement.value);
    
            let feedbackElement = currentExercise.querySelector(".feedback");
            if (userAnswer === correctAnswer) {
                feedbackElement.innerHTML = "<span style='color: green;'>✅ Correct!</span>"; // Đáp án đúng
    
                // Hiển thị nút "Next" và "Replay"
                let nextBtn = currentExercise.querySelector(".nextBtnHidden");
                let replayBtn = currentExercise.querySelector(".replayBtn");
    
                nextBtn.style.display = "inline-block";
                replayBtn.style.display = "inline-block";
    
                // Ẩn nút "Check" và "Skip"
                let checkBtn = currentExercise.querySelector(".checkBtn");
                let skipBtn = currentExercise.querySelector(".skipBtn");
                checkBtn.style.display = "none";
                skipBtn.style.display = "none";
    
            } else {
                let feedback = checkSpelling(userAnswer, correctAnswer);
                feedbackElement.innerHTML = "<span style='font-size: 20px;'>❌ Incorrect </span><br><span>" + feedback + "</span>"; // Đáp án sai
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

document.addEventListener("DOMContentLoaded", function () {
    const dropdownBtn = document.querySelector('.dropdown-btn');
    const dropdown = dropdownBtn.closest('.dropdown');
    
    dropdownBtn.addEventListener('click', function() {
        dropdown.classList.toggle('active'); // Toggle the 'active' class on the dropdown
    });
});

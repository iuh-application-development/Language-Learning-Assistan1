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
    
    function correctPartialAnswer(userAnswer, correctAnswer) {
        let userWords = userAnswer.split(' ');
        let correctWords = correctAnswer.split(' ');
        let fixedWords = [];
    
        for (let i = 0; i < correctWords.length; i++) {
            let correctWord = correctWords[i];
            let userWord = userWords[i] || '';
            let fixedWord = '';
    
            for (let j = 0; j < userWord.length; j++) {
                if (userWord[j].toLowerCase() === correctWord[j]?.toLowerCase()) {
                    fixedWord += correctWord[j];  // Giữ nguyên ký tự chuẩn
                } else {
                    break;  // Dừng nếu sai
                }
            }
    
            fixedWords.push(fixedWord);
        }
    
        return fixedWords.join(' ').trim();
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
            if (currentExerciseIndex < totalExercises - 1) {
                currentExerciseIndex++;
                updateExerciseDisplay();
            } else {
                // ✅ Nếu là bài cuối → hiện navigation box chuyển subtopic
                const navBox = document.getElementById("navigation-box");
                if (navBox) navBox.style.display = "flex";
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
                let originalCorrect = currentExercise.dataset.correct;
                userInputElement.value = originalCorrect;
                userInputElement.style.color = "inherit";
                userInputElement.style.textDecoration = "none";
                userInputElement.classList.remove("input-highlight");

                feedbackElement.innerHTML = `<div style="color: green; font-weight: bold;">✅ You are correct!</div>`;
    
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
                if (currentExerciseIndex === totalExercises - 1) {
                    const completionBox = document.getElementById("completion-dialog");
                    if (completionBox) {
                        completionBox.style.display = "block";
                        completionBox.scrollIntoView({ behavior: "smooth" });
                    }
                }
            } else {
                let feedback = checkSpelling(userAnswer, correctAnswer);
                feedbackElement.innerHTML = "<span style='font-size: 20px;'>❌ Incorrect </span><br><span>" + feedback + "</span>";
            
                let fixedInput = correctPartialAnswer(userAnswer, currentExercise.dataset.correct);
                userInputElement.value = fixedInput;
                userInputElement.style.color = "black";
                userInputElement.style.textDecoration = "underline dashed orange";
                userInputElement.style.textDecorationThickness = "2px";
            
                let correctWords = currentExercise.dataset.correct.split(' ');
                let fixedWords = fixedInput.split(' ');
                let feedbackHTML = '';
            
                for (let i = 0; i < correctWords.length; i++) {
                    if (fixedWords[i]) {
                        feedbackHTML += `<span class="correct-word">${correctWords[i]}</span> `;
                    } else {
                        feedbackHTML += '*'.repeat(correctWords[i].length) + ' ';
                    }
                }
            
                feedbackElement.innerHTML = `
                    <div style='font-size: 20px; color: orange;'>⚠️ Incorrect</div>
                    <div style='margin-top: 8px;'>${feedbackHTML.trim()}</div>
                `;
            }
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            const activeElement = document.activeElement;
    
            if (activeElement && activeElement.classList.contains("userInput")) {
                event.preventDefault(); // ❌ Không cho xuống dòng
    
                const exerciseBox = activeElement.closest(".exercise-box");
                const checkBtn = exerciseBox.querySelector(".checkBtn");
    
                if (checkBtn && checkBtn.style.display !== "none") {
                    checkBtn.click(); // ✅ Gọi lại logic kiểm tra
                }
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

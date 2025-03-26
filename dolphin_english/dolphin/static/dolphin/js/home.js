document.addEventListener("DOMContentLoaded", function() {
    // Lấy các phần tử
    var modal = document.getElementById("featuresModal");
    var btn = document.getElementById("openModal");
    var close = document.querySelector(".close-overlay");

    // Khi người dùng bấm vào nút "Bắt đầu ngay", mở modal
    btn.addEventListener("click", function(e) {
        e.preventDefault(); // Ngăn việc gọi trang web khác
        modal.style.display = "flex"; // Hiển thị modal
    });

    // Khi người dùng bấm vào nút đóng (x), đóng modal
    close.addEventListener("click", function() {
        modal.style.display = "none"; // Ẩn modal
    });

    // Khi người dùng bấm ngoài modal, đóng modal
    window.addEventListener("click", function(event) {
        if (event.target == modal) {
            modal.style.display = "none"; // Ẩn modal khi bấm ngoài
        }
    });
});

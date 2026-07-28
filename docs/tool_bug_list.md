# 📋 DANH SÁCH CÁC TRƯỜNG HỢP LỖI CỦA CÔNG CỤ (TOOL FAILURE MODES)

*   **Dự án:** Trợ Lý Tư Vấn Khóa Học Sinh Viên (Đề tài 7)
*   **Tệp kiểm tra:** [tools.py](file:///c:/workspace/LAB/AITHUCCHIEN/LABS/K4-Day03-B3-2-E403/src/tools.py)

---

Dưới đây là phân tích các trường hợp lỗi (Failure Modes) có thể xảy ra khi Agent gọi các công cụ trong `src/tools.py`. Các lỗi này được chia làm 3 nhóm chính: **Lỗi do dữ liệu đầu vào từ Agent/User**, **Lỗi logic nghiệp vụ bên trong**, và **Lỗi cấu trúc/dữ liệu hệ thống giả lập**.

---

## 📥 NHÓM 1: LỖI DO DỮ LIỆU ĐẦU VÀO CỦA AGENT/USER (INPUT-BASED FAILURE MODES)

### 1. Lỗi định dạng thời gian trong lịch bận (`check_schedule_conflict`)
*   **Mô tả:** Tham số `unavailable_slots` chứa slot có định dạng giờ không phải "HH:MM" (ví dụ: `"8:00"` thay vì `"08:00"`, hoặc `"8h00"`, `"18h-20h"`).
*   **Nguyên nhân:** Hàm `_time_to_minutes` sử dụng `time_text.split(":")` và chuyển đổi trực tiếp `int()`.
*   **Hậu quả:** Gây ra lỗi `ValueError: not enough values to unpack` hoặc `ValueError: invalid literal for int()`. Công cụ sẽ bị bắt ngoại lệ và trả về chuỗi thông báo lỗi kỹ thuật hệ thống thay vì hướng dẫn Agent sửa lại format.

### 2. Lỗi không đồng bộ ngôn ngữ/tên ngày trong tuần (`check_schedule_conflict`)
*   **Mô tả:** Người dùng hoặc Agent truyền tên ngày trong tuần bằng tiếng Anh (ví dụ: `"Saturday"`, `"Monday"`) hoặc viết tắt (`"T7"`, `"CN"`) thay vì tiếng Việt chuẩn hóa (`"Thứ Bảy"`, `"Thứ Hai"`).
*   **Nguyên nhân:** Hàm so sánh trực tiếp chuỗi sau khi chuẩn hóa chữ thường: `_normalize_text(slot["day"]) == _normalize_text(course_schedule["day"])`. Dữ liệu hệ thống dùng tiếng Việt (`"Thứ Hai"`, `"Thứ Ba"`...).
*   **Hậu quả:** Không tìm thấy sự trùng khớp ngày, dẫn đến công cụ trả về `"KHÔNG TRÙNG LỊCH"` mặc dù thực tế có trùng. Đây là lỗi logic cực kỳ nguy hiểm vì Agent sẽ tư vấn sai cho sinh viên.

### 3. Lỗi kiểu dữ liệu không khớp (Type Mismatch ở các tham số tùy chọn)
*   **Mô tả:** Agent truyền sai kiểu dữ liệu của các tham số. Ví dụ: truyền `max_fee` là chuỗi `"2000000"` thay vì số nguyên `2000000`, hoặc truyền `completed_courses` chứa phần tử không phải chuỗi.
*   **Hậu quả:**
    *   **Đối với `search_courses`:** Phép so sánh `course["fee"] > max_fee` sẽ ném ra `TypeError` (so sánh giữa `int` và `str`). Mặc dù lỗi này được bắt ở block `except Exception`, công cụ vẫn trả về thông báo lỗi hệ thống chung chung và không tìm kiếm được.
    *   **Đối với `check_prerequisites`:** Phần tử không phải chuỗi sẽ được ép kiểu bằng `str(item)` nhưng có thể tạo ra các giá trị rác như `"NONE"` hoặc `"[OBJECT OBJECT]"` khiến việc kiểm tra điều kiện tiên quyết bị sai lệch.

### 4. Lỗi so sánh danh sách môn học không tồn tại (`compare_courses`)
*   **Mô tả:** Agent truyền vào danh sách chứa các mã môn học không tồn tại trong hệ thống (ví dụ: `["CS101", "UNKNOWN999"]`).
*   **Hậu quả:** Hàm sẽ trả về thông báo `"KHÔNG TÌM THẤY: Các mã khóa học không tồn tại: UNKNOWN999."` và dừng toàn bộ tiến trình so sánh, ngay cả khi các môn học còn lại trong danh sách (như `"CS101"`) hoàn toàn hợp lệ.

---

## 🧠 NHÓM 2: LỖI LOGIC NGHIỆP VỤ BÊN TRONG (BUSINESS LOGIC FAILURE MODES)

### 1. Bỏ qua môn học bị thiếu trong lộ trình đề xuất (`recommend_learning_path`)
*   **Mô tả:** Khi một môn học trong lộ trình mặc định (ví dụ: `"MATH101"`) không tồn tại trong `COURSE_DATABASE`.
*   **Nguyên nhân:** Trong vòng lặp đề xuất, hàm kiểm tra `if course is not None:` rồi mới append vào kết quả.
*   **Hậu quả:** Môn học bị thiếu sẽ bị bỏ qua một cách im lặng (silently ignored). Sinh viên nhận được một lộ trình khuyết thiếu thông tin mà Agent không hề nhận biết được lỗi thiếu hụt dữ liệu môn học nền tảng này.

### 2. Trùng giờ học tuyệt đối (Edge case về thời gian kết thúc và bắt đầu)
*   **Mô tả:** Một môn học kết thúc lúc `11:00` và môn tiếp theo bắt đầu lúc `11:00`.
*   **Nguyên nhân:** Hàm `_is_time_overlap` so sánh: `max(start_1, start_2) < min(end_1, end_2)`.
*   **Hậu quả:** Đối với trường hợp giáp ranh (`11:00 < 11:00` là `False`), hàm trả về không trùng lịch. Tuy nhiên trên thực tế, sinh viên không thể di chuyển hoặc chuyển lớp ngay lập tức trong cùng 1 phút (đặc biệt nếu học offline). Tuy đây đúng về mặt toán học nhưng chưa tối ưu về mặt nghiệp vụ tư vấn thực tế.

### 3. So sánh học phí và tín chỉ rỗng (`compare_courses`)
*   **Mô tả:** Logic tìm kiếm môn học rẻ nhất/nhiều tín chỉ nhất dựa vào hàm `min()` và `max()` trên danh sách `found_courses`.
*   **Hậu quả:** Nếu danh sách rỗng (do không tìm thấy môn học nào hợp lệ), hàm `min()` và `max()` trên list rỗng sẽ ném ra lỗi `ValueError: min() arg is an empty sequence`. Lỗi này sẽ bị bắt bởi ngoại lệ hệ thống chung, làm hỏng toàn bộ phản hồi của tool.

### 4. Lỗi xử lý đa mục tiêu học tập (`recommend_learning_path`)
*   **Mô tả:** Khi sinh viên có nhu cầu tích hợp (ví dụ: muốn học cả "Web" và "AI" để làm Full-stack AI Web App).
*   **Nguyên nhân:** Logic của hàm `recommend_learning_path` sử dụng cấu trúc rẽ nhánh loại trừ `if-elif-else`.
*   **Hậu quả:** Hệ thống chỉ nhận diện được mục tiêu đầu tiên khớp từ khóa và bỏ qua hoàn toàn mục tiêu còn lại, trả về lộ trình đơn mục tiêu thay vì kết hợp hoặc cảnh báo.

### 5. Lỗi trùng lặp danh sách môn học khi so sánh (`compare_courses`)
*   **Mô tả:** Agent truyền vào danh sách chứa các mã môn học trùng lặp (ví dụ: `["CS101", "CS101", "MATH101"]`).
*   **Hậu quả:** Tool vẫn thực hiện so sánh bình thường cho cùng một môn học, dẫn đến kết quả trả về bị lặp thông tin vô nghĩa, gây lãng phí token của LLM và làm nhiễu thông tin phản hồi cho sinh viên.

---

## 🗄️ NHÓM 3: LỖI DO CẤU TRÚC DỮ LIỆU HỆ THỐNG GIẢ LẬP (DATABASE INTEGRITY FAILURE MODES)

### 1. Thiếu trường thông tin bắt buộc trong cấu trúc database giả lập
*   **Mô tả:** File dữ liệu hoặc danh sách `COURSE_DATABASE` có một khóa học bị thiếu trường thông tin (ví dụ: thiếu key `schedule`, `fee`, `prerequisites` hoặc `skills`).
*   **Hậu quả:**
    *   `search_courses`: Gây lỗi `KeyError` khi cố truy cập `course["skills"]` hoặc `course["fee"]`.
    *   `get_course_details`: Gây lỗi `KeyError` khi truy cập `course["schedule"]` hoặc `course["prerequisites"]`.
    *   Mặc dù các lỗi này đều được bọc trong block `except Exception`, nó khiến tool hoàn toàn mất khả năng hoạt động đối với các bản ghi lỗi thay vì chỉ bỏ qua bản ghi lỗi đó và tiếp tục làm việc với các bản ghi hợp lệ khác.

### 2. Xung đột kiểu dữ liệu trong thuộc tính khóa học
*   **Mô tả:** Thuộc tính `fee` hoặc `credits` trong `COURSE_DATABASE` bị nhập nhầm thành kiểu chuỗi (ví dụ: `"1500000"` hoặc `"3"`).
*   **Hậu quả:** Làm sai lệch các phép toán so sánh hoặc tính toán tự động trong `compare_courses` hoặc bộ lọc `max_fee` trong `search_courses`, dẫn đến lỗi runtime bị ném ra và tool trả về thông báo thất bại.

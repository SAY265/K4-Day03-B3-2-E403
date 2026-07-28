# 📊 BÁO CÁO GIÁM SÁT & ĐÁNH GIÁ (OBSERVABILITY TRACE LOGS)
*Dành cho Role 5: Observability & Reviewer*

---

## 🎯 1. BẢNG CHẤM ĐIỂM AGENTIC FIT (SCORING MATRIX)

| Tiêu chí | Điểm (1-5) | Lý do đánh giá |
| :--- | :---: | :--- |
| 🧠 **Multi-step Reasoning** | `4/5` | Cần suy luận logic đa bước: kiểm tra điều kiện tiên quyết, phân tích tiến độ tích lũy tín chỉ và đề xuất lộ trình học phù hợp với năng lực sinh viên. |
| 🛠️ **Tool Interaction** | `5/5` | Cần tra cứu dữ liệu thời gian thực qua API hệ thống quản lý đào tạo (lịch mở lớp, danh sách môn học, số lượng slot còn lại, bảng điểm sinh viên). |
| 🔀 **Dynamic Decision** | `4/5` | Lịch trình và lựa chọn thay đổi linh hoạt theo kết quả tra cứu (ví dụ: nếu lớp đầy/trùng lịch thì tự động tìm môn thay thế hoặc chuyển sang ca học khác). |
| ⏳ **Long Horizon** | `3/5` | Quy trình tư vấn kéo dài qua nhiều bước (thu thập nguyện vọng $\rightarrow$ tra cứu điểm $\rightarrow$ lọc môn học $\rightarrow$ xếp thời khóa biểu không trùng $\rightarrow$ hoàn thiện lộ trình). |
| **TỔNG ĐIỂM FIT** | **17/20** | **KẾT LUẬN: BÀI TOÁN RẤT NÊN DÙNG REACT AGENT!** |

---

## 🔍 2. SO SÁNH PHẢN HỒI (TEST CASE #3)

**Câu hỏi**: *"Tôi muốn đăng ký môn Nhập môn Khai phá Dữ liệu học kỳ này, kiểm tra giúp tôi xem tôi đã đủ điều kiện môn tiên quyết chưa?"*

### 🤖 Chatbot Baseline:
* **Phản hồi**: *"Phản hồi giả lập offline cho bài test."*
* **Nhận xét**: Không biết thông tin thực tế, bị ảo giác.

### 🧠 ReAct Agent:
* **Thought 1**: Sinh viên muốn đăng ký môn "Nhập môn Khai phá Dữ liệu" và muốn kiểm tra điều kiện tiên quyết. Để làm được điều này, tôi cần mã môn học của môn này trước, sau đó hỏi sinh viên về các môn đã hoàn thành để kiểm tra tiên quyết.
* **Action 1**: `search_courses[keyword="Nhập môn Khai phá Dữ liệu"]`
* **Observation 1**: `KHÔNG TÌM THẤY: Không có khóa học nào phù hợp với các tiêu chí đã cung cấp.`
* **Thought 2**: Tôi không tìm thấy môn "Nhập môn Khai phá Dữ liệu" với từ khóa chính xác. Có thể tên môn học không hoàn toàn khớp hoặc có thể có tên tiếng Anh. Tôi sẽ thử tìm kiếm với từ khóa chung hơn như "Khai phá Dữ liệu".
* **Action 2**: `search_courses[keyword="Khai phá Dữ liệu"]`
* **Observation 2**: `KHÔNG TÌM THẤY: Không có khóa học nào phù hợp với các tiêu chí đã cung cấp.`
* **Thought 3**: Tôi sẽ thử tìm kiếm với một từ khóa tiếng Anh phổ biến cho lĩnh vực này là "Data Mining" để mở rộng phạm vi tìm kiếm.
* **Action 3**: `search_courses[keyword="Data Mining"]`
* **Observation 3**: `KHÔNG TÌM THẤY: Không có khóa học nào phù hợp với các tiêu chí đã cung cấp.`
* **Thought 4**: Tôi đã thử nhiều từ khóa khác nhau nhưng đều không tìm thấy khóa học trong hệ thống dữ liệu. Vì vậy, tôi không thể kiểm tra điều kiện tiên quyết vì chưa có đủ thông tin về môn học.
* **Final Answer**: *"Rất tiếc, tôi không thể tìm thấy khóa học 'Nhập môn Khai phá Dữ liệu' trong hệ thống của mình với các từ khóa đã thử. Bạn có thể vui lòng cung cấp thêm thông tin hoặc tên chính xác của khóa học để tôi kiểm tra điều kiện tiên quyết cho bạn?"*
* **Nhận xét**: Agent đã thể hiện khả năng suy luận đa bước và thử nhiều cách truy vấn khác nhau, nhưng vẫn chưa thể hoàn thành nhiệm vụ vì dữ liệu môn học và tiên quyết chưa có trong hệ thống.


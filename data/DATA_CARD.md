# Data card — dữ liệu bản chạy thử B2

> Bản đầu CP2, 27/11/2026. Dữ liệu demo không thay cho tư vấn của dược sĩ/bác sĩ. Chỉ dùng thông tin có nguồn; không suy ra liều hay khẳng định thuốc an toàn khi chưa thấy tương tác trong dữ liệu.

## Dataset 1 · Ghi chú thuốc và an toàn có nguồn

| | |
|---|---|
| Dùng để làm gì | Seed cho tra cứu thuốc, kiểm tra một tương tác đã có nguồn và nhận diện trường hợp cần chuyển dược sĩ; hỗ trợ tạo câu thử sau này |
| Từ đâu | Tóm lược ngắn từ MedlinePlus (NIH/NLM), Cục Quản lý Dược/Bộ Y tế và thông tin thuốc công khai của Long Châu. Xem danh sách nguồn bên dưới; với thuốc cụ thể cần kiểm lại đúng tờ hướng dẫn của sản phẩm trước khi đưa vào bản chạy |
| Xử lý những bước gì | Chọn thông tin tổng quát liên quan đến hoạt chất, nguy cơ và chuyển chuyên môn; không chép nguyên tài liệu; không đưa lời khuyên liều dùng cá nhân; nhà thuốc và tình huống demo được dựng |
| Số dòng / số đoạn | 13 bản ghi (5 ban đầu, 6 thuốc bổ sung, 2 tương tác) và 5 quy tắc lịch trong `data/b2_seed.json` |
| Phiên bản / ngày lấy | Bản seed CP2, 27/11/2026; URL được ghi trong từng bản ghi |
| Nhãn | Kết hợp thông tin có nguồn và ca demo `synthetic`; xem rõ từng bản ghi |
| Giới hạn | Chưa phải danh mục tương tác đầy đủ; có 2 cặp levothyroxine với calcium/iron yêu cầu tách thời điểm theo nhãn. `eval_bucket=moderate_timing_separation` chỉ là nhóm kiểm thử nội bộ, không phải phân loại mức độ lâm sàng. Chưa có cặp nhẹ được xác minh. Hệ thống chỉ được xếp lịch từ đơn người dùng và các ràng buộc có nguồn; thiếu dữ kiện thì hỏi thêm/chuyển dược sĩ |

### Nguồn công khai

- MedlinePlus, **Ibuprofen Drug Information**: cảnh báo NSAID như ibuprofen có thể gây loét/xuất huyết tiêu hóa và cần thông báo cho bác sĩ/dược sĩ về các thuốc dùng cùng: <https://medlineplus.gov/druginfo/meds/a682159.html>
- MedlinePlus, **Warfarin Drug Information**: thông tin về nguy cơ chảy máu và việc thuốc/TP bổ sung khác có thể ảnh hưởng nguy cơ chảy máu khi dùng warfarin: <https://www.medlineplus.gov/druginfo/meds/a682277.html>
- Nhà thuốc Long Châu, **Ibuprofen 200 mg**: trang thông tin thuốc nêu phối hợp ibuprofen với warfarin làm tăng nguy cơ chảy máu dạ dày: <https://nhathuoclongchau.com.vn/thuoc/ibuprofen-200-nadyphar-10x10-19637.html>
- Cục Quản lý Dược, **Quyết định 696/QĐ-QLD**: tài liệu hướng dẫn tư vấn sử dụng thuốc, nhấn mạnh cung cấp hướng dẫn phù hợp và tham khảo tờ hướng dẫn: <https://dav.gov.vn/upload_images/files/696_QD_QLD.pdf>
- Cục Quản lý Dược, **tài liệu công bố về paracetamol** (tham khảo để xác định cần kiểm tra đúng sản phẩm/tờ HDSD, không dùng thay nhãn sản phẩm): <https://dav.gov.vn/upload_images/files/0466_2017_XNQC.pdf>
- MedlinePlus, **Levothyroxine Drug Information**: thời điểm dùng, tên thương mại và tách calcium/iron ít nhất 4 giờ: <https://medlineplus.gov/druginfo/meds/a682461.html>
- DailyMed, **Levothyroxine Sodium Tablets**: calcium carbonate và ferrous sulfate có thể giảm hấp thu; nhãn hướng dẫn cách nhau ít nhất 4 giờ: <https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=0b94e62c-eb04-47fd-b6ec-a70c588d7cd7>
- MedlinePlus, **Calcium Carbonate Drug Information**: cách dùng theo nhãn, dùng cùng bữa ăn khi là thực phẩm bổ sung và tên thương mại: <https://medlineplus.gov/druginfo/meds/a601032.html>
- MedlinePlus, **Iron Supplements Drug Information**: các dạng muối sắt và một số tên thương mại: <https://medlineplus.gov/druginfo/meds/a682778.html>
- DailyMed, **Metformin Hydrochloride Tablets**: hướng dẫn dùng cùng bữa ăn cho dạng viên được trích dẫn: <https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1e8136e0-cc98-41e4-ad4b-a8fc27fb4daa>
- MedlinePlus, **Amlodipine Drug Information**: dùng mỗi ngày cùng hoặc không cùng thức ăn, vào khoảng cùng thời điểm: <https://medlineplus.gov/druginfo/meds/a692044.html>
- MedlinePlus, **Omeprazole Drug Information**: thời điểm khác nhau theo dạng kê đơn/không kê đơn: <https://medlineplus.gov/druginfo/meds/a693050.html>

## Dataset 2 · Ca hội thoại demo

| | |
|---|---|
| Dùng để làm gì | Kiểm tra luồng hỏi lại khi thiếu thông tin, chuyển dược sĩ, và không bịa lịch dùng thuốc |
| Từ đâu | Nhóm tự viết, dữ liệu giả lập có seed trong `data/b2_seed.json` |
| Xử lý những bước gì | Không chứa người thật; tên nhà thuốc và bối cảnh được dựng; các trường hợp chỉ minh họa luồng, không phải bằng chứng pain hay dữ liệu lâm sàng |
| Số dòng / số đoạn | 2 tình huống demo |
| Phiên bản / ngày lấy | Bản seed CP2, 27/11/2026; seed cố định `MNTS-B2-CP2-v1` |
| Nhãn | `synthetic` |
| Giới hạn | Không dùng để khuyến nghị thuốc, liều, khoảng cách uống hoặc chẩn đoán. Các ca thiếu dữ kiện phải dẫn tới hỏi thêm hoặc chuyển người có chuyên môn |

**Cách tạo/kiểm:** viết tay theo các trường hợp luồng ở `spec.md` §5; không sinh dữ liệu người bệnh. Nhóm cần kiểm thủ công từng thông tin y khoa với nguồn trước khi bật tra cứu tương ứng. Tên nhà thuốc trong ca demo là hư cấu.

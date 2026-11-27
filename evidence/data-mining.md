# Đào review ứng dụng nhà thuốc — CP3

## 1. Nguồn và cách lấy mẫu

- Nguồn chính: trang đánh giá App Store của ứng dụng Long Châu, <https://apps.apple.com/vn/app/long-ch%C3%A2u-chuy%C3%AAn-gia-thu%E1%BB%91c/id1586071844?see-all=reviews>.
- Ngày kiểm tra: 27/11/2026. Trang hiển thị 10 review khác nhau trong lần kiểm tra này; mã R01–R10 theo thứ tự hiển thị. Không tính phần lặp của cùng review trong giao diện. Không lưu tên tài khoản.
- Đối chiếu riêng: trang Google Play <https://play.google.com/store/apps/details?hl=vi&id=vn.frt.longchau.app> hiển thị 3 review được đọc trong lần kiểm tra; không gộp vào mẫu số App Store vì tập hiển thị và cơ chế chọn review khác nhau.
- Đây là mẫu thuận tiện do cửa hàng ứng dụng chọn hiển thị, không ngẫu nhiên, nhỏ và có review cũ. Kết quả chỉ mô tả các review đã xem, không đại diện người dùng ứng dụng.

## 2. Quy tắc mã hóa — xác định trước khi đếm

- Đơn vị: một review duy nhất.
- Gán `order_or_app_friction=1` nếu nội dung nêu trở ngại khi đặt/nhận thuốc hoặc dùng ứng dụng để hoàn tất việc đó: xử lý chậm, lỗi thao tác/thanh toán, đơn bị hủy/không giao, hoặc không truy cập được.
- Không tính lời khen hoặc vấn đề riêng tư vào chỉ số này. Mỗi review chỉ được tính tối đa một lần; R07 được ghi riêng vì nói về thao tác thông tin trên điện thoại, không phải trở ngại giao dịch.
- Bảng mã dưới đây cho phép kiểm lại số đếm bằng cách áp dụng cùng tiêu chí cho 10 review ở URL trên. Chỉ lưu tóm tắt ngắn, không lưu tên tài khoản.

| Mã | Ngày review | Mã hóa | Lý do ngắn |
|---|---|---:|---|
| R01 | 19/09/2021 | 0 | Nêu app vẫn giao thuốc; trải nghiệm tích cực |
| R02 | 03/03/2022 | 0 | Khen tư vấn và tiện ích ứng dụng |
| R03 | 13/05/2024 | 1 | Nêu xử lý chậm |
| R04 | 19/06/2022 | 0 | Đánh giá thao tác/đặt nhanh |
| R05 | 07/10/2023 | 1 | Đơn đã xác nhận nhưng bị hủy, không báo |
| R06 | 14/07/2024 | 1 | App đơ, thanh toán lỗi; khó sửa/hủy đơn |
| R07 | 21/05/2023 | Riêng | Nêu nhân viên thao tác/cài ứng dụng và nhập thông tin trên điện thoại; không tính vào chỉ số giao dịch |
| R08 | 15/08/2024 | 1 | Nêu đơn thuốc không được giao và phải liên hệ hỗ trợ |
| R09 | 10/11/2025 | 1 | Nêu giao trễ và khó yêu cầu hoàn tiền |
| R10 | 25/01/2025 | 1 | Nêu không truy cập được ứng dụng/trang web |

## 3. Kết quả

| Chỉ báo | x / N | Tỷ lệ | Diễn giải |
|---|---:|---:|---|
| Review mô tả trở ngại đặt/nhận thuốc hoặc hoàn tất thao tác trên app | 6 / 10 | 60% | Chỉ trong 10 review App Store được xem; không đại diện toàn bộ người dùng |
| Review tích cực về giao thuốc, tư vấn, tiện lợi hoặc tốc độ | 3 / 10 | 30% | Cùng mẫu trên |
| Review nêu vấn đề riêng tư/thao tác dữ liệu (theo dõi riêng) | 1 / 10 | 10% | R07; không cộng vào chỉ báo trở ngại giao dịch |

Đối chiếu phụ: cả 3 review Google Play được đọc đều nêu chậm giao/đáp ứng hoặc trải nghiệm ứng dụng kém (3/3 review đang hiển thị). Không gộp thành tỷ lệ chung với App Store.

## 4. Ví dụ ngắn, đã bỏ tên tài khoản

- R03: “Xử lý cực kỳ chậm”
- R05: “tự ý huỷ đơn hàng”
- R06: “thanh toán lỗi”
- R08: “đơn thuốc chưa được giao”
- R09: “không nhận lại được tiền”
- R10: “không vào dc kể cả trên web?”

Các trích đoạn trên là lời người dùng đăng công khai, được giữ ngắn để minh họa mã hóa; chúng không phải lời phỏng vấn và không nêu tên người viết.

## 5. Giới hạn của mẫu Long Châu

Review được mã hóa nói về đặt hàng, giao nhận, hỗ trợ và độ ổn định ứng dụng. Chúng **không chứng minh** người chăm sóc gặp khó khi kiểm tra tương tác thuốc hoặc xếp lịch dùng thuốc, cũng không cho biết tần suất người thân phải sắp thuốc. Vì vậy, 6/10 chỉ là tín hiệu về trở ngại trải nghiệm ứng dụng nhà thuốc, không được dùng để kết luận giả thuyết pain B2 đúng.

Khảo sát 20 người được tổng hợp riêng tại `evidence/survey/results.csv` và `evidence/summary.md`; khảo sát hỏi về mức độ không chắc khi làm theo hướng dẫn đã có, nhưng không kiểm tra trực tiếp việc rà soát tương tác thuốc. Chưa có phỏng vấn. Không suy diễn review Long Châu thành bằng chứng trực tiếp cho pain B2.

## 6. Tìm kiếm bổ sung có chủ đích — review về quản lý nhiều thuốc

- Nguồn: review hiển thị trên [Medisafe App Store (Mỹ)](https://apps.apple.com/us/app/medisafe-medication-management/id573916946?see-all=reviews) và [Medisafe Google Play](https://play.google.com/store/apps/details?hl=en_IN&id=com.medisafe.android.client), kiểm tra ngày 27/11/2026.
- Cách chọn: tìm trong trang review các bài có nhắc trực tiếp đến nhiều thuốc/khác thời điểm, người chăm sóc cùng quản lý lịch, nhắc thuốc trùng hoặc thất bại, hay khó nhập/xem chỉ dẫn. Đây là **mẫu chọn có chủ đích**, không phải mẫu ngẫu nhiên; không tính tỷ lệ và không cộng vào 10 review Long Châu.
- Ghi chú phạm vi: đây là người dùng một ứng dụng quốc tế, phần lớn review bằng tiếng Anh; các bài cho thấy những tình huống có thể xảy ra, không đại diện người chăm sóc Việt Nam hay chứng minh độ phổ biến của pain.

| Mã | Nền tảng / ngày hiển thị | Chủ đề | Trích dẫn ngắn đã bỏ tên |
|---|---|---|---|
| M01 | App Store / 31-07 (năm không hiện trong phần review) | Người dùng mô tả lịch của nhiều thuốc với khoảng cách khác nhau gây rối; review nói app đã giúp họ tạo lịch. Đây vừa là ví dụ về pain vừa là phản ví dụ cho giả thuyết app không giúp được. | “very confusing” |
| M02 | App Store / 08-06-2024 | Người chăm sóc chia sẻ trách nhiệm với chồng; trạng thái đã đánh dấu ở thiết bị này nhưng thiết bị kia vẫn nhắc, và thiết lập nhiều người chăm sóc chưa trực quan. | “already marked” |
| M03 | App Store / 23-11-2021 | Người dùng không tìm được cách nhập hướng dẫn dạng 1 hoặc 2 viên mỗi lần và bỏ cuộc. | “given up” |
| M04 | App Store / 06-10 (năm không hiện trong phần review) | Review mô tả nhận nhắc lại thuốc đã đánh dấu đã uống và suýt uống liều thứ hai. | “already marked as taken” |
| M05 | Google Play / 14-08-2026 | Người dùng nói nhắc âm thanh không hoạt động ở vài thời điểm đã đặt và họ bỏ lỡ liều; sau đó đặt app khác làm dự phòng. | “missed doses” |
| M06 | App Store / 19-01-2022 | Người dùng chăm sóc con gái và nêu phép tính nhắc mua lại không xử lý đúng lịch chỉ dùng thuốc vào cuối tuần. | “refill reminder calculation” |
| M07 | App Store / 18-06-2022 | Người viết nói đã dùng mục kiểm tra tương tác rồi gọi dược sĩ để hỏi thêm. Đây là lời kể cá nhân, không xác minh được kết quả y khoa hay mức độ chính xác của cảnh báo. | “call the pharmacist” |

Các đoạn trích ngắn được lấy từ review công khai; không lưu tên tài khoản, tên thuốc, bệnh hay chi tiết điều trị. Review M01 và M02 cho thấy tính năng có thể giúp sắp xếp, còn M02–M07 nêu các khó khăn hoặc tình huống liên quan đến phối hợp người chăm sóc, nhập hướng dẫn, độ tin cậy nhắc lịch và cần kiểm tra tương tác. Vì thế đây là bằng chứng định tính sát hơn với B2, nhưng chưa phải bằng chứng định lượng hay khảo sát trực tiếp người chăm sóc tại Việt Nam.

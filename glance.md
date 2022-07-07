1. Glance:
- Glane (Image Service) là image service cung cấp khả năng discovering, registering (đăng ký), retrieving (thu thập) các image cho virtual machine. OpenStack Glance là central repository cho virtual image.
- Glance cung cấp RESTful API cho phép querying VM image metadata cũng như thu thập các actual image.
- VM image có sẵn thông qua Glance có thể stored trong nhiều vị trí khác nhau, từ file system đến object storage system như OpenStack Swift OpenStack.
- Trong Glance, images được lưu trữ như template, được sử dụng để launching new instances. Glance được thiết kế để trở thành một service độc lập đối với các user cần tổ chức large virtual disk images. Glance cung cấp giải pháp end-to-end cho cloud disk image management. Nó cũng có thể lấy các bản snapshots từ running instance cho việc backing up VM và các states của VM.

2. Glance Component
- Glance có các components:
	+ glance-api: chấp nhận API calls cho việc tìm kiếm, lấy và lưu trữ image.
    + glance-registry: thực hiện lưu trữ, xử lý và lấy thông tin metadata của image.
    + database: lưu trữ metadata của image.
    + storage repository: tích hợp với nhiều thanh phần của OpenStack như file systems, Amazon S3 và HTTP cho image storages.

![](https://www.sparkmycloud.com/blog/wp-content/uploads/2016/01/Untitled-drawing2.png)

- Glance chấp nhận API request cho image từ end-users hoặc Nova components và có thể stores nó trong object storage service,swift hoặc storage repository khác.
- Image server hỗ trợ các back-end stores:
	+ File system
    + OpenStack Image server lưu trữ virtual machine images trong file system back end là default.Đây là back end đơn giản lưu trữ image files trong local file system.
    + Object Storage: Là hệ thống lưu trữ do OpenStack Swift cung cấp - dịch vụ lưu trữ có tính sẵn sàng cao , lưu trữ các image dưới dạng các object.
    + Block Storage: Hệ thống lưu trữ có tính sẵn sàng cao do OpenStack Cinder cung cấp, lưu trữ các image dưới dạng block.
    + VMware: ESX/ESXi or vCenter Server target system.
    + S3: The Amazon S3 service.
    + HTTP: OpenStack Image service có thể đọc virtual machine images mà có sẵn trên Internet sử dụng HTTP. Đây là store chỉ đọc.
    + RADOS Block Device(RBD): Stores images trong Ceph storage cluster sử dụng Ceph’s RBD interface.
    + Sheepdog: A distributed storage system dành cho QEMU/KVM.
    + GridFS: Stores images sử dụng MongoDB.

3. Glance Architecture
- Glance có client-service architecture và cung cấp Rest API để request đến server được thực hiện. Request từ client được chấp nhận thông qua Rest API và chờ Keystone authentication. Glance Domain controller quản lý tất cả các hoạt động internal, là phân chia đến layers, mỗi layer thực hiện nhiệm vụ của nó.
Glance store là layer giao tiếp giữa glance và storage backends bên ngoài hoặc local file system và cung cấp uniform interface để truy cập. Glance sử dụng SQL central Database làm điểm truy cập cho mỗi components khác trong hệ thống.
- The Glance architecture gồm các thành phần khác nhau:
    + Client : bất kỳ ứng nào sử dụng Glance server.
    + REST API : gửi request tới Glance thông qua REST.
    + Database Abstraction Layer (DAL) : application programming interface mà hợp nhất việc giao tiếp giữa Glance và databases.
    + Glance Domain Controller : middleware thực hiện các chức năng chính của Glance: authorization, notifications, policies, database connections.
    + Glance Store : tổ chức việc tương tác giữa Glance và các hệ thống data stores khác.
    + Registry Layer : optional layer tổ chức việc giao tiếp bảo mật giữa domain và DAL sử dụng một service riêng biệt.

![](https://www.sparkmycloud.com/blog/wp-content/uploads/2016/01/Untitled-drawing11.png)

3. Glance Formats

![](https://cdn.statically.io/img/3.bp.blogspot.com/-EGKwj3WyVVU/W0NwACwgpZI/AAAAAAAAG3E/HY-tohrVjssBSxhfMWIetk-v8HF6MCHKACLcBGAs/s1600/disk.png?quality=100&f=auto)

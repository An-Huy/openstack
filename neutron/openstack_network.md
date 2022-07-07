1. OpenStack Networking
- OpenStack Networking cho phép bạn tạo và quản lý network objects, như networks, subnets, và ports.  
- Networking service, tên là **neutron**, cung cấp API cho php bạn xác định kết nối mạng và địa chỉ trong cloud. Networking service cho phép các nhà vận hành vận dụng các công nghệ networking khác để cung cấp cho cloud networking của họ. Networking service cũng cung cấp API để cấu hình và quản lý nhiều dịch vụ mạng khác nhau, từ L3 forwarding và NAT đến load balancing, firewalls, và virtual private networks.  
- Nó bao gồm các thành phần:  
    + API server: OpenStack Networking API bao gồm hỗ trợ **Layer 2 networking** và **IP address management (IPAM)**, cũng như 1 phần mở rộng cho **Layer 3 router** cho phép routing giữa các **Layer 2 networking**. OpenStack Networking bao gồm 1 danh sách các plug-in cho phép tương tác với các công nghệ mạng mã nguồn mở khác nhau, bao gồm routers, virtual switches, và software-defined networking (SDN) controllers.
    + OpenStack Networking plug-in và agents: Plugs và unplugs ports, tạo network hoặc subnets, và cung cấp địa chỉ IP. Plug-in và agents được chọn khác nhau tùy thuộc và nhà cung cấp và công nghệ được sử dụng trong cloud cụ thể. Điều quan trọng cần đề cập là chỉ có thể sử dụng 1 plug-in trong 1 thời điểm.  
- Messaging queue: Cấp nhận và định tuyến các yêu cầu RPC giữa các agents để hoàn thành các hoạt động API. Message queue là được sử dụng trong **Ml2 plug-in** cho RPC giữa neutron server và neutron agents chạy trên mỗi hypervisor, **ML2 mechanism drivers** cho **Open vSwitch** và **Linux bridge**.  

![](https://docs.openstack.org/install-guide/_images/network1-overview.png)

![](https://docs.openstack.org/install-guide/_images/network1-connectivity.png)

* Provider networks: Provider network cung cấp khả năng kết nối layer-2 đến instance với sự hỗ trợ tùy chọn cho DHCP và metadata service. Mạng này kết nối, hoặc map, với các mạng layer-2 hiện có trong data center, thường sử dụng tính năng VLAN (802.1q) tagging để xác định và tách chúng.  
- Provider network cung cấp nói chung cung cấp sự đơn giản, hiệu năng và độ tin cậy với chi phí linh hoạt. Bởi mặc định, chỉ có admin có thể tạo hoặc cập nhật các **provider network** bởi vì cấu hình yêu cầu của cở sở hạ tầng physical network. 

![](https://docs.openstack.org/install-guide/_images/network2-overview.png)

![](https://docs.openstack.org/install-guide/_images/network2-connectivity.png)

* Self-service networks: **Self-service networks** chủ yếu cho phép các projects chung (không có đặc quyền) để quản lý mạng mà không cần đến admin. Các mạng này hoàn toàn là virtual và yêu câu virtual routers tương tác với provider và các mang bên ngoai Internet. **Self-service networks** cũng thường cung cấp các DHCP và metadata services đến instances.  
- Trong hầu hết các trường hợp, self-service networks sử dụng *overlay protocol* như VXLAN và GRE bởi vì chung có thể hỗ trợ nhiều mạng hơn layer-2 segementation bang cách sử dụng VLAN tagging (802.1q). Hơn nữa, các VLAN thường yêu cầu cấu hình bổ sung của cơ sở hạ tầng mạng vật lý.  
- IPv4 **self-service network** sử dụng dải địa chỉ private IP và tương tác với **provider network** thông qua *source NAT* trên **virtual routers**. **Địa chỉ Floating IP** cho phép truy cập đến instance từ provider networks thông *destionation NAT* trên **virtual router**.   
- **Networking serive** thực hện routers bằng cách sử dụng **layer-3 agent**, thường là ít nhất 1 **network node**. Trái ngược với **provider network** cung cấp kết nối instances đến mạng vật lý tại layer-2, **self-service networks** phải đi qua **later-3 agent**.  
- **Flat**: Tất cả instances tren cùng 1 mạng, cũng có thể chia sẻ với các hosts. Không có VLAN tagging hoặc phần chia mạng.  
- **VLAN**: Mạng cho phéo user tạo nhiều provider hoặc project sử dụng VLANIDs (802.1Q) tương ứng với các VLAN có trong mạng vật lý.  
- **GRE và VXLAN**: VXLAN và GRE là giao thức đóng gói tọa ra overkay network để kích hoạt và kiểm soát giữa compute instance. 1 networking router được yêu cầu để cho phép luông lưu lượng đu ra ngoài mạng GRE hoặc VXLAN. 1 router cũng được yêu cầu để kết nối trực tiếp *project network* với *external network*. Router cung cấp khả năng kết nối trực tiếp instance từ external network sử dụng **địa chỉ floating IP**.  

* Ports: Port là điểm để kết nối để gắn 1 thiết bị, chẳng hạn NIC của virtual server, đến virtual network. Port cũng mô tả cấu hình mạng liên quan, chả hạn như MAC và địa chỉ IP được sử dụng trên port đó.
* Routers: cung cấp virtual layer-3 services như routing và NAT giữa **self-service network** và **provider network** hoặc giữa các **self-service networks** phụ thuộc vào project. Networking service sử dụng **layer-3 agent** để quản lý routers thông qua namespaces.  
- **Security groups**:  cung cấp vùng lưu trữ cho *virtual firewall rules* để kiểm soát lưu lượng truy cập ingress (inbound to instance) và egress (outbound from instance) mạng ở mức port. **Security groups** sử dụng default deny policy và chỉ chứa các rules đồng ý phép lưu lượng cụ thể. FIrewall driver chuyển các *group rule* đến cấu hình cho ciing chệ lọc gói bên dưới như `iptables`.  
- Mỗi project có chứa 1 `default` security group mà cho phép tát cả lưu lượng egress và từ chối tất cả các lưu lượng ingress. Bạn có thể thay đổi rules trong `default` security group. Nó bạn launch instance mà không có security group chỉ định, `default` security group sẽ tự động được áp dụng cho instance đó. Tương tự, nếu bạn tạo 1 port mà không chỉ định security group, `default` security group tự động được áp cho port đó.  

* Agents
- Cung cấp layer 2/3 đến các instance.  
- Xử lý chuyển tiếp physical-virtual network.  
- Xử lý metadata, etc.
* Layer 2 (Ethernet và Switching): Linux Bridge, OVS 
* Layer 3 (IP và Routing): L3, DHCP  

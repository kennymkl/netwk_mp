import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress; 
import java.net.SocketException;

public class Client {
    private DatagramSocket datagramSocket;
    private InetAddress inetAddress;
    private byte[] buffer;

    public Client(DatagramSocket datagramSocket, InetAddress inetAddress) {
        this.datagramSocket = datagramSocket;
        this.inetAddress = inetAddress;
    }

    public void sendThenReceive(){

        Scanner scanner = new Scanner(System.in);
        String username = "";
        boolean isConnected = false;
        
        while(true){
            try{
                String messageToSend = scanner.nextLine();
                
                // Check for join command
                if (messageToSend.startsWith("/join")){
                    String[] tokens = messageToSend.split(" ");
                    if (tokens.length == 3){
                        String serverIpAddress = tokens[1];
                        int port = Integer.parseInt(tokens[2]);
                        inetAddress = InetAddress.getByName(serverIpAddress);
                        datagramSocket = new DatagramSocket();
                        isConnected = true;
                        System.out.println("Connection to the Message Board Server is successful!");
                    } else {
                        System.out.println("Error: Invalid command syntax. Usage: /join <server_ip_add> <port>");
                    }
                }
                
                // Check for other commands or regular messages
                else if (isConnected){
                    if (messageToSend.startsWith("/leave")){
                        DatagramPacket datagramPacket = new DatagramPacket(buffer, buffer.length, inetAddress, 1234);
                        datagramSocket.send(datagramPacket);
                        datagramSocket.close();
                        isConnected = false;
                        System.out.println("Connection closed. Thank you!");
                    } else {
                        // Convert message to JSON and send to server
                        JSONObject jsonObject = new JSONObject();
                        jsonObject.put("username", username);
                        jsonObject.put("message", messageToSend);
                        String jsonString = jsonObject.toString();
                        buffer = jsonString.getBytes();
                        DatagramPacket datagramPacket = new DatagramPacket(buffer, buffer.length, inetAddress, 1234);
                        datagramSocket.send(datagramPacket);
                        
                        // Receive response from server
                        datagramSocket.receive(datagramPacket);
                        String messageFromServer = new String(datagramPacket.getData(), 0, datagramPacket.getLength());
                        System.out.println("Server: " + messageFromServer);
                    }
                } else {
                    System.out.println("Error: You must connect to the server first. Usage: /join <server_ip_add> <port>");
                }
            } catch (IOException e){
                e.printStackTrace();
                break;
            }
        }
    }

    public static void main(String[] args) {
        DatagramSocket datagramSocket = new DatagramSocket();
        InetAddress inetAddress = InetAddress.getByName("localhost");
        Client client = new Client(datagramSocket, inetAddress);
        System.out.println("Send datagram packets to a server.");
        client.sendThenReceive();
    }
}
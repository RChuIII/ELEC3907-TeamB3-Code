using UnityEngine;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class SocketRecieve: MonoBehaviour{
    Thread receiveThread;
    public int port = 5052;
    public bool startReceiving = true;
    public bool p2c = false;
    public string data;

    public void Start(){
        receiveThread = new Thread(new ThreadStar(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }

    public void ReceiveData(){
        client = new UdpClient(port);
        while(startReceiving){
            try{
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any,0);
                Byte dataByte= client.Receive(ref anyIP);
                data = Encoding.UTF8.GetString(dataByte);
                if (p2c) { print(data); }
            } catch (Exception e){
                print(e.ToString());
            }
        }
    }
}
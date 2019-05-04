using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class CameraController : MonoBehaviour {

// 1. Declare Variables

	Thread receiveThread;
	UdpClient client;
	int port;
	float angleX;
	float angleY;
	Vector3 rotateValue;
	public float rotationSpeed = 10f;

	// 2. Initialize variables
	void Start () 	
	{
  		port = 5065;
  		InitUDP();
	}

	// 3. InitUDP
	private void InitUDP()
	{
  		print ("UDP Initialized");

  		receiveThread = new Thread (new ThreadStart(ReceiveData));
  		receiveThread.IsBackground = true;
  		receiveThread.Start();
	}
	// 4. Receive Data
	private void ReceiveData()
	{
  	client = new UdpClient (port); //1
  	while (true) //2
  	{
   		try
  		{
      	IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("0.0.0.0"), port);
      	byte[] data = client.Receive(ref anyIP);

      	string text = Encoding.UTF8.GetString(data);
      	print (">> " + text);
		//string dummytext = "2n6";
		// camera control here
		add(text);

    	} 
    	catch(Exception e)
    	{
      	print (e.ToString());
    	}
  }
}
	// add data
	private void add(string text)
	{
		int splitN = text.IndexOf("n");
		// set angles by splitting string
		angleX = float.Parse(text.Substring(0, splitN));
		angleY = float.Parse(text.Substring(splitN+1, text.Length -1 -splitN));
		print("X = " + angleX + "Y = " + angleY);
	}
	// rotate camera

	void LateUpdate () 
	{
		// get angle vector
		rotateValue = new Vector3(-angleY, angleX, 0);
		// rotate
		transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.Euler(rotateValue), rotationSpeed*Time.deltaTime);
	}

	void Update()
    {
        // check button "s" to abort the read-thread
        if (Input.GetKeyDown("x"))
            stopThread();
    }

    // Unity Application Quit Function
    void OnApplicationQuit()
    {
        stopThread();
    }

    // Stop reading UDP messages
    private void stopThread()
    {
        if (receiveThread.IsAlive)
        {
            receiveThread.Abort();
        }
        client.Close();
    }

}

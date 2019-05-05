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
	float zoom;
	Vector3 rotateValue, moveVal;
	public float rotationSpeed = 5f;
	public float threshHold = 0f;

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
		string[] arr = text.Split('n');
		angleX = float.Parse(arr[0]);
		angleY = float.Parse(arr[1]);
		zoom = float.Parse(arr[2]);
		print("X = " + angleX + " Y = " + angleY + " A = " + zoom);
	}
	
	// rotate camera
	void LateUpdate () 
	{
		// get angle vector
		rotateValue = new Vector3(-angleY, angleX, 0);
		// get move vector
		moveVal = new Vector3(0f, 0f, zoom);

		Vector3 currentRotation = transform.rotation.eulerAngles;
		Vector3 angleChange = currentRotation - rotateValue;
		Vector3 zoomChange = transform.position - moveVal;

		// // move in z
		// if(zoomChange.magnitude >= 2f){
		// 	transform.position = Vector3.Lerp(new Vector3 (0f,0f,0f), moveVal, 0.1f*Time.deltaTime);
		// }
		

		// rotate
		if(angleChange.magnitude >= threshHold){
			transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.Euler(rotateValue), rotationSpeed*Time.deltaTime);
		}
		
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

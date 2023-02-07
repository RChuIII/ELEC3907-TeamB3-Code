using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Tracking : MonoBehaviour{
    public SocketRecieve sockrec;
    public GameObject[] joints;

    void Start(){

    }

    void Update(){
        string data = sockrec.data;
        data = data.Remove(0,1);
        data = data.Remove(data.Length()-1, 1);
        string[] angles = data.Split(",");
        
    }
}
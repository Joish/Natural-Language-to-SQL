import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { RequestOptions, Request, RequestMethod } from '@angular/http';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})

export class UploadComponent  {

  title = 'Natural Language -> Structured Query Language';

  public evts = {};
  public file: File = null;
  serverData: JSON;
  employeeData: JSON;

  //constructor(private http: HttpClient) { }

  // sayHi(et) {
  //   this.http.post('http://127.0.0.1:5002/uploader', {
  //     title: 'foo',
  //     body: 'bar',
  //     userId: 1
  //   })
  //     .subscribe(
  //     res => {
  //       console.log(res);
  //     },
  //     err => {
  //       console.log("Error occured");
  //     }
  //     );
  // }

  onChange(event) {
    // console.log(event.target.file[0]);
    this.evts = event.target.files[0];
    this.file = <File>event.target.files[0];
    console.log(this.file)
  }

  request()
  {
    console.log('asds')
  }

}



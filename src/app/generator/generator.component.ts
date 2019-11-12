import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { RequestOptions, Request, RequestMethod } from '@angular/http';
import { Observable } from 'rxjs/internal/Observable';


@Component({
  selector: 'app-generator',
  templateUrl: './generator.component.html',
  styleUrls: ['./generator.component.css']
})
export class GeneratorComponent implements OnInit {

  result = null;
  cloumn = null;
  queryresult = null;

  returnRes = null;

  constructor(private http:HttpClient) { }

  ngOnInit() {
    this.http.get(" http://127.0.0.1:5002/columnvalues").subscribe(res => {
      this.cloumn = res;
    });

    this.http.get(" http://127.0.0.1:5002/result").subscribe(res => {
      this.result = res;
    });


    this.http.get(" http://127.0.0.1:5002/query_result").subscribe(res => {
      // console.log(res.length)
      this.queryresult = res;
      console.log(this.queryresult)
    

    });

    console.log(this.queryresult)
  }

  resultCall()
  {
    this.http.get(" http://127.0.0.1:5002/result").subscribe(res =>{
      this.result = res;
    });
  }

  callFunction()
  {
    console.log("call function")
    this.resultCall()
  }


  // alert(result)


}

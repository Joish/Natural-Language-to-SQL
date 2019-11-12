import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { UploadComponent } from './upload/upload.component';
import { GeneratorComponent } from './generator/generator.component';
import { BadrequestComponent } from './badrequest/badrequest.component';

import { HttpClientModule } from '@angular/common/http';
import { EmptyComponent } from './empty/empty.component';


@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    UploadComponent,
    GeneratorComponent,
    BadrequestComponent,
    EmptyComponent,
    
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

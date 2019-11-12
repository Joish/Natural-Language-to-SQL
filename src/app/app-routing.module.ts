import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { NavbarComponent } from 'src/app/navbar/navbar.component';
import { UploadComponent } from 'src/app/upload/upload.component';
import { GeneratorComponent } from 'src/app/generator/generator.component';
import { BadrequestComponent } from 'src/app/badrequest/badrequest.component';
import { EmptyComponent } from './empty/empty.component';


const routes: Routes = [
  {
    path: '',
    component:UploadComponent
  },
  {
    path: 'generator',
    component: GeneratorComponent
  },
  {
    path: 'bad_request',
    component: BadrequestComponent
  },
  {
    path: 'empty',
    component: EmptyComponent
  },


];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

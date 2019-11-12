import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BadrequestComponent } from './badrequest.component';

describe('BadrequestComponent', () => {
  let component: BadrequestComponent;
  let fixture: ComponentFixture<BadrequestComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BadrequestComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BadrequestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

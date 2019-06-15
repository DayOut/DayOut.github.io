import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgbModalModule, NgbDropdownModule } from '@ng-bootstrap/ng-bootstrap';
import { CalendarModule, DateAdapter } from 'angular-calendar';
import { adapterFactory } from 'angular-calendar/date-adapters/date-fns';

import { FullcalendarComponent } from './fullcalendar.component';
import { FullcalendarRoutes } from './fullcalendar.routing';

@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(FullcalendarRoutes),
    CalendarModule.forRoot({
      provide: DateAdapter,
      useFactory: adapterFactory
    }),
    FormsModule,
    NgbDropdownModule
  ],
  declarations: [FullcalendarComponent]
})
export class FullcalendarModule {}

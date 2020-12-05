import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DndDirective } from './dnd.directive';
import { ProgressComponent } from './progress/progress.component';
import { AngularFireModule } from '@angular/fire';
import { AngularFireStorageModule, AngularFireStorageReference, AngularFireUploadTask } from "@angular/fire/storage";

import { MatChipsModule } from '@angular/material/chips'
import { AngularFireStorage } from 'angularfire2/storage';
import { HttpClientModule } from '@angular/common/http';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { firebaseConfig } from '../assets/firebaseconfig';

@NgModule({
  declarations: [
    AppComponent,
    DndDirective,
    ProgressComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AngularFireStorageModule,
    AngularFireModule.initializeApp(firebaseConfig),
    MatChipsModule,
    HttpClientModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
    BrowserAnimationsModule,
  ],
  providers: [AngularFireStorage, MatSnackBarModule],
  bootstrap: [AppComponent]
})
export class AppModule { }

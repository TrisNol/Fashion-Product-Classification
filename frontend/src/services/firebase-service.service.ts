import { Injectable } from '@angular/core';
import { v4 as uuid } from 'uuid';
import { AngularFireStorage } from '@angular/fire/storage';
import { map, finalize, timeout, catchError } from "rxjs/operators";
import { Subscription, Observable, Subject, throwError } from 'rxjs';
import { EventEmitter } from 'protractor';

@Injectable({
  providedIn: 'root'
})
export class FirebaseServiceService {

  public downloadUrlEvent = new Subject<string>();

  constructor(private afStorage: AngularFireStorage ) {}

  uploadFileToFirebase(file) {
    let path: string;
    const id = this.tokenGenerator();
    path = '/images/'
    let date:Date;
    date = new Date();
    path = path + id;
    path = path + '-';
    path = path + date.getTime();
    path = path +'.jpg';
    const fileRef = this.afStorage.ref(path);
    let task = this.afStorage.upload(path, file);
    task
    .snapshotChanges()
    .pipe(
      timeout(5000),
      finalize(() => {
        let downloadURL = fileRef.getDownloadURL();
        downloadURL.subscribe(url => {
          this.downloadUrlEvent.next(url)
        });
      }),
      catchError(err => {
        return throwError(err);
      })
    )
    .subscribe(url => {
      if (url) {
        console.log(url);
      }
    });

    return path;
  }

  tokenGenerator() {
    let refToken: string;
    const myId = uuid();
    refToken = myId;

    return refToken;
  }
}

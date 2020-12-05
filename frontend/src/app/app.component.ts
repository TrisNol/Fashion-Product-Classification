import { Component, ViewChild, ElementRef } from '@angular/core';
import { FirebaseServiceService } from 'src/services/firebase-service.service';
import { ApiService } from 'src/core/services/api.service';
import { throwError } from 'rxjs';
import { SnackbarService } from './snackbar.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  [x: string]: any;
  title = 'IHK-Webseite';
  @ViewChild("fileDropRef", { static: false }) fileDropEl: ElementRef;
  files: any[] = [];
  working = false;
  hasError = false;
  errorMessage: string;

  tags: Array<Array<string>> = [];

  constructor(private firebaseServiceService: FirebaseServiceService, private apiService: ApiService, private snackServie: SnackbarService) {
    this.firebaseServiceService.downloadUrlEvent.subscribe(url => {
      this.files[this.files.length - 1].url = url;
      this.apiService.getCategories(url).subscribe(
        res => { this.tags.push(res['categories']); 
        this.working = false;},
        err => {
          this.hasError = true;
          this.errorMessage = err.message;
          this.working = false;
          snackServie.openSnackbar("Something went wrong, please try again later!");
        },
      );
    })
  }

  /**
   * on file drop handler
   */
  onFileDropped($event) {
    //this.uploadFileToFirebase($event);
    this.prepareFilesList($event);
    console.log(this.files.length);
    this.working = true;
  }

  /**
   * handle file from browsing
   */
  fileBrowseHandler(files) {
    //this.uploadFileToFirebase(files);
    this.prepareFilesList(files);
    console.log(this.files.length);
    this.working = true;
  }

  /**
   * Delete file from files list
   * @param index (File index)
   */
  deleteFile(index: number) {
    if (this.files[index].progress < 100) {
      console.log("Upload in progress.");
      return;
    }
    this.files.splice(index, 1);
    this.tags.splice(index, 1);
  }
  uploadFilesSimulator(index: number) {
    setTimeout(() => {
      if (index === this.files.length) {
        return;
      } else {
        const progressInterval = setInterval(() => {
          if (this.files[index].progress === 100) {
            clearInterval(progressInterval);
            this.uploadFilesSimulator(index + 1);
          } else {
            this.files[index].progress += 5;
          }
        }, 200);
      }
    }, 1000);
  }

  /**
   * Convert Files list to normal array list
   * @param files (Files List)
   */
  prepareFilesList(files: Array<any>) {
    for (const item of files) {
      var ext = item.name.substr(item.name.lastIndexOf('.') + 1);
      if(ext !='jpg') {
        this.snackServie.openSnackbar("App only supports .jpg files");
        this.working = false;
        return;
      }
      item.progress = 0;
      this.files.push(item);
      try {
        this.uploadFileToFirebase(item);
        this.error = false;
      } catch (error) {
        this.hasError = true;
        this.errorMessage = error.message;
        this.working = false;
        this.snackServie.openSnackbar(this.errorMessage);
      }
    }
    this.fileDropEl.nativeElement.value = "";
    this.uploadFilesSimulator(0);
    files = [];
  }
  /**
  * format bytes
  * @param bytes (File size in bytes)
  * @param decimals (Decimals point)
  */
  formatBytes(bytes, decimals = 2) {
    if (bytes === 0) {
      return "0 Bytes";
    }
    const k = 1024;
    const dm = decimals <= 0 ? 0 : decimals;
    const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
  }

  uploadFileToFirebase(event) {
    try {
      let s: string;
    s = this.firebaseServiceService.uploadFileToFirebase(event);
    } catch (error) {
      throwError(error);
    }
  }
}

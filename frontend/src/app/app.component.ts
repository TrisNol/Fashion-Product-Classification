import { Component, ElementRef, ViewChild } from '@angular/core';
import { throwError } from 'rxjs';
import { ApiService } from './services/api.service';
import { SnackbarService } from './snackbar.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss'],
    standalone: false
})
export class AppComponent {
  title = 'IHK-Webseite';
  @ViewChild("fileDropRef", { static: false }) fileDropEl: ElementRef | undefined;
  files: any[] = [];
  working = false;
  hasError = false;
  errorMessage: string = "";

  tags: Array<Array<string>> = [];

  constructor(private apiService: ApiService, private snackServie: SnackbarService) {
  }

  /**
   * on file drop handler
   */
  onFileDropped($event: any | undefined) {
    if ($event) {
      this.prepareFilesList($event);
      this.working = true;
    }
  }

  /**
   * handle file from browsing
   */
  fileBrowseHandler(event: any | undefined) {
    let files = event.files;
    if (files) {
      this.prepareFilesList(files);
      this.working = true;
    }
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
  }

  /**
   * Convert Files list to normal array list
   * @param files (Files List)
   */
  prepareFilesList(files: Array<any>) {
    for (const item of files) {
      var ext = item.name.substr(item.name.lastIndexOf('.') + 1);
      if (ext != 'jpg') {
        this.snackServie.openSnackbar("App only supports .jpg files");
        this.working = false;
        return;
      }
      this.apiService.convertFile(item).subscribe(imageBase64 => this.files.push({ progress: 100, url: 'data:image/jpeg;base64,' + imageBase64 }));
      try {
        this.categorizeImage(item);
      } catch (error: any) {
        this.hasError = true;
        this.errorMessage = error.message;
        this.working = false;
        this.snackServie.openSnackbar(this.errorMessage);
      }
    }
    this.fileDropEl!.nativeElement.value = "";
    this.uploadFilesSimulator(0);
    files = [];
  }
  /**
  * format bytes
  * @param bytes (File size in bytes)
  * @param decimals (Decimals point)
  */
  formatBytes(bytes: number, decimals = 2) {
    if (bytes === 0) {
      return "0 Bytes";
    }
    const k = 1024;
    const dm = decimals <= 0 ? 0 : decimals;
    const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
  }

  categorizeImage(file: File) {
    try {
      this.apiService.convertFile(file).subscribe(image => {
        this.apiService.categorizeImage(image).subscribe(res => {
          this.tags.push(res['categories']);
          this.working = false;
        });
      })
    } catch (error) {
      console.log(error);
      throwError(error);
    }
  }
}

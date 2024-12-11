// api.service.ts
import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { firstValueFrom } from 'rxjs';

@Injectable()
export class ApiService {
  constructor(private readonly httpService: HttpService) {}

  async getData(): Promise<any> {
    const url = 'https://jsonplaceholder.typicode.com/posts';
    try {
      const response = await firstValueFrom(this.httpService.get(url));
      return response.data; // API 응답 데이터 반환
    } catch (error) {
      throw new Error(`API 요청 실패: ${error.message}`);
    }
  }

  async postData(data: any): Promise<any> {
    const url = 'https://jsonplaceholder.typicode.com/posts';
    try {
      const response = await firstValueFrom(this.httpService.post(url, data));
      return response.data; // API 응답 데이터 반환
    } catch (error) {
      throw new Error(`API 요청 실패: ${error.message}`);
    }
  }
}

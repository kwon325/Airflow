// app.controller.ts
import { Controller, Get, Post, Body } from '@nestjs/common';
import { ApiService } from './api.service';

@Controller('api')
export class AppController {
  constructor(private readonly apiService: ApiService) {}

  @Get('data')
  async getData() {
    return await this.apiService.getData();
  }

  @Post('data')
  async postData(@Body() data: any) {
    return await this.apiService.postData(data);
  }
}

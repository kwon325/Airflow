// app.module.ts
import { Module } from '@nestjs/common';
import { HttpModule } from '@nestjs/axios';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ApiService } from './api.service';

@Module({
  imports: [HttpModule],
  controllers: [AppController],
  providers: [AppService, ApiService],
})
export class AppModule {}

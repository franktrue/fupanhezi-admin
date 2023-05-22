/*
 * @创建文件时间: 2021-08-23 22:05:53
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-08-23 22:11:52
 * 联系Qq:1638245306
 * @文件介绍: 定时任务详情
 */

import { request } from '@/api/service'

export const urlPrefix = '/api/dvadmin_celery/task_detail/'

export function GetList (query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  })
}
export function AddObj (obj) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}

export function UpdateObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}
export function DelObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'delete',
    data: obj
  })
}

// 开启/暂停任务
export function UpdateStatus (obj) {
  return request({
    url: urlPrefix + 'update_status/' + obj.id + '/',
    method: 'post',
    data: obj
  })
}

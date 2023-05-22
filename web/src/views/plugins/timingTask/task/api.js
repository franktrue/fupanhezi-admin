/*
 * @创建文件时间: 2021-08-02 22:53:41
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-08-23 22:06:56
 * 联系Qq:1638245306
 * @文件介绍:
 */
import { request } from '@/api/service'

export const urlPrefix = '/api/dvadmin_celery/task/'

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

export function BatchDel (keys) {
  return request({
    url: urlPrefix + 'multiple_delete/',
    method: 'delete',
    data: { keys }
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

// 执行任务
export function RunTask (obj) {
  return request({
    url: urlPrefix + 'run_task/' + obj.id + '/',
    method: 'post',
    data: obj
  })
}

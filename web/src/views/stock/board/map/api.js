import { request } from '@/api/service'
import XEUtils from 'xe-utils'
export const urlPrefix = '/api/stock/board/map/'

/**
 * 列表查询
 */
export function GetList (query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  })
}
/**
 * 新增
 */
export function createObj (obj) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}

/**
 * 修改
 */
export function UpdateObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}
/**
 * 删除
 */
export function DelObj (id) {
  return request({
    url: urlPrefix + id + '/',
    method: 'delete',
    data: { id }
  })
}

export function FetchData(obj) {
  return request({
    url: urlPrefix + 'fetch/',
    method: 'post',
    data: obj
  })
}

export function BatchData(obj) {
  return request({
    url: urlPrefix + 'batch/',
    method: 'post',
    data: obj
  })
}


export function BatchAllData(obj) {
  return request({
    url: urlPrefix + 'batchAll/',
    method: 'post',
    data: obj
  })
}

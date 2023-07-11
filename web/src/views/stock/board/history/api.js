import { request } from '@/api/service'
import XEUtils from 'xe-utils'
export const urlPrefix = '/api/stock/board/history/'

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

export function FetchAll(obj) {
  return request({
    url: urlPrefix + 'fetch_all/',
    method: 'post',
    data: obj
  })
}

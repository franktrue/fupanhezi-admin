import { request } from '@/api/service'

export const urlPrefix = 'api/stock/gnn_subject/'

/**
 * 列表查询
 */
export function GetList (query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: { ...query }
  }).then(res => {
    // 将列表数据转换为树形数据
    return res
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

// 同步
export function FetchObj () {
  return request({
    url: urlPrefix + 'fetch/',
    method: 'post'
  })
}

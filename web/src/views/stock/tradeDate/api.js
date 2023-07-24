import { request } from '@/api/service'
export const urlPrefix = '/api/stock/trade_date/'

export function GetList(query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  })
}

export function AddObj(obj) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}

export function UpdateObj(obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}

export function DelObj(id) {
  return request({
    url: urlPrefix + id + '/',
    method: 'delete',
    data: { id }
  })
}

// 更新交易日
export function FetchData(obj) {
  return request({
    url: urlPrefix + "fetch/",
    method: 'post'
  })
}


// 清除缓存
export function DeleteCache(obj) {
  return request({
    url: urlPrefix + "del_cache/",
    method: 'post',
    data: obj
  })
}


// 清除最新板块排序缓存
export function DeleteLatestBoardCache() {
  return request({
    url: urlPrefix + "del_latest_board_cache/",
    method: 'post'
  })
}

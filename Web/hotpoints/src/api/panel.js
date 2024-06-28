import request from '@/utils/request'

// 热点榜单数据
export function getHotPointList() {
    return request({
        url: '/hotlist',
        method: 'GET'
    })
}

// 热度上升榜
export function getSpeedList() {
    return request({
        url: '/speedlist',
        method: 'GET'
    })
}
import request from '@/utils/request'

// 获取话题详情
export function getTopicDetail(id) {
    return request({
        url: '/topic/details',
        method: 'GET',
        params: {
            topicID: id
        }
    })
}

// 获取近5日访问量
export function getTopicVisits(id) {
    return request({
        url: '/topic/5days',
        method: 'GET',
        params: {
            topicID: id
        }
    })
}

// 获取话题内帖子信息
export function getPostList(id) {
    return request({
        url: '/topic/postlist',
        method: 'GET',
        params: {
            topicID: id
        }
    })
}

// 获取评论分类
export function getComment(id) {
    return request({
        url: '/topic/comment',
        method: 'GET',
        params: {
            topicID: id
        }
    })
}

// 获取事件图谱
export function getMap(id) {
    return request({
        url: '/topic/map',
        method: 'GET',
        params: {
            topicID: id
        }
    })
}
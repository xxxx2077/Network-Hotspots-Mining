<template>
    <div style="width: 100%; height: 100%;">
        <RelationGraph ref="graphRef" :options="graphOption"></RelationGraph>
    </div>
</template>

<script>
import RelationGraph from 'relation-graph'
export default {
    name: 'Relation',
    components: {
        RelationGraph,
    },
    data() {
        return {
            graphOption: {
                debug: false,
                defaultNodeBorderWidth: 0,
                allowSwitchLineShape: true,
                allowSwitchJunctionPoint: true,
                defaultLineShape: 1,
                'layouts': [
                    {
                        'label': '自动布局',
                        'layoutName': 'force',
                        'layoutClassName': 'seeks-layout-force'
                    }
                ],
                defaultJunctionPoint: 'border'
            }
        }
    },
    mounted() {
        this.showGraph();
    },
    beforeDestroy() {
        this.$refs.graphRef.getInstance().stopAutoLayout();
    },
    methods: {
        showGraph() {
            const jsonData = {
                rootId: 'a',
                nodes: [
                    { id: '1', text: 'A' },
                    { id: '2', text: 'B' },
                    { id: '3', text: 'C' },
                    { id: '4', text: 'E' }
                ],
                lines: [
                    { from: '1', to: '2', text: '关系1' },
                    { from: '1', to: '3', text: '关系2' },
                    { from: '1', to: '4', text: '关系3' },
                    { from: '2', to: '4', text: '关系4' }
                ]
            }

            this.$refs.graphRef.setJsonData(jsonData, (graphInstance) => {
                graphInstance.setZoom(30);
            });
        },
    }
}
</script>
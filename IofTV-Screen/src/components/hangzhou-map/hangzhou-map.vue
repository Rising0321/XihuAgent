<template>
  <div class="hangzhou-map">
    <div id="osm-map" class="map-container"></div>
    <div v-if="mapError" class="map-error">{{ mapError }}</div>
  </div>
</template>

<script>
export default {
  name: 'HangzhouMap',
  data() {
    return {
      map: null,
      mapError: null,
      blueOverlay: null,
      isMapInitialized: false
    }
  },
  mounted() {
    console.log('地图组件已挂载');
    this.initMap()
  },
  beforeDestroy() {
    // 在组件销毁前清除事件监听
    if (this.map) {
      window.removeEventListener('resize', this.handleResize);
      this.map.remove();
      this.map = null;
    }
  },
  methods: {
    initMap() {
      // 如果地图已经初始化，就不再重复初始化
      if (this.isMapInitialized) {
        console.log('地图已初始化，跳过');
        return;
      }
      
      console.log('初始化地图开始');
      // 确保Leaflet脚本已加载
      if (typeof L === 'undefined') {
        console.log('Leaflet未加载，开始加载脚本');
        this.loadLeafletScript(() => {
          console.log('Leaflet脚本加载完成');
          this.createMap()
        })
      } else {
        console.log('Leaflet已加载，直接创建地图');
        this.createMap()
      }
    },

    loadLeafletScript(callback) {
      // 如果已加载过，就不再重复加载
      if (document.querySelector('link[href*="leaflet.css"]')) {
        callback();
        return;
      }
      
      // 加载Leaflet CSS
      const leafletCSS = document.createElement('link')
      leafletCSS.rel = 'stylesheet'
      leafletCSS.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
      document.head.appendChild(leafletCSS)

      // 加载Leaflet脚本
      const script = document.createElement('script')
      script.type = 'text/javascript'
      script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
      script.onload = callback
      script.onerror = () => {
        this.mapError = "Leaflet脚本加载失败";
        console.error("Leaflet脚本加载失败");
      }
      document.head.appendChild(script)
    },

    createMap() {
      try {
        if (this.isMapInitialized || this.map) {
          console.log('地图已创建，跳过');
          return;
        }
        
        console.log('开始创建地图');
        const mapContainer = document.getElementById('osm-map');
        if (!mapContainer) {
          this.mapError = "找不到地图容器元素";
          console.error("找不到地图容器元素");
          return;
        }
        
        // 西湖坐标 [纬度, 经度]
        const westLakeCoords = [30.242828, 120.142404]
        
        // 创建地图实例 - 简化版，减少功能
        this.map = L.map('osm-map', {
          center: westLakeCoords,
          zoom: 11, // 降低缩放级别以显示更大范围
          zoomControl: false,
          attributionControl: false,
          // 极端性能优化选项
          preferCanvas: true,
          renderer: L.canvas({ padding: 0.5 }),
          fadeAnimation: false,
          markerZoomAnimation: false,
          zoomAnimation: false,
          inertia: false,
          boxZoom: false,
          doubleClickZoom: false,
          keyboard: false,
          scrollWhenFocus: false,
          dragging: false, // 禁用拖动，固定地图位置
          touchZoom: false,
          tap: false,
          worldCopyJump: false
        });

        console.log('地图实例创建成功');
        
        // 使用更轻量的瓦片源，或直接用一张静态图
        const tileUrl = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png';
        
        // 显著扩大加载范围，确保覆盖整个容器区域
        // 杭州市大致边界范围，大幅扩展左右范围
        const hangzhouBounds = L.latLngBounds(
          L.latLng(29.95, 119.50), // 西南角，向西扩展 
          L.latLng(30.50, 121.10)  // 东北角，向东扩展
        );
        
        // 创建一个静态的预加载瓦片集
        const tiles = L.tileLayer(tileUrl, {
          maxZoom: 11,
          minZoom: 11,
          updateWhenIdle: true,
          updateWhenZooming: false,
          keepBuffer: 12, // 增加缓冲，确保加载更多瓦片
          tileSize: 256,
          bounds: hangzhouBounds, // 加载比实际视图更大的区域
          noWrap: true
        }).addTo(this.map);
        
        // 手动设置地图视图以包含整个杭州区域，添加额外的填充
        this.map.fitBounds(hangzhouBounds, {
          animate: false,
          padding: [-100, -100] // 负填充以展示更大区域
        });
        
        // 禁用瓦片动画
        tiles.on('loading', function() {
          // 设置瓦片样式为即时显示，无淡入效果
          document.querySelectorAll('.leaflet-tile-loaded').forEach(tile => {
            tile.style.transition = 'none';
            tile.style.opacity = '1';
          });
        });

        // 添加视觉效果填充整个容器
        this.applySimpleOverlay();

        // 只添加最基本的缩放控件
        L.control.zoom({
          position: 'topright',
          zoomInText: '+',
          zoomOutText: '-',
          zoomInTitle: '放大',
          zoomOutTitle: '缩小'
        }).addTo(this.map);

        console.log('地图创建完成');

        // 不添加resize监听，使用一次性的尺寸设置
        this.map.invalidateSize();
        
        // 一次性加载完成后禁用地图交互
        setTimeout(() => {
          // 锁定地图视图
          this.map.setMinZoom(11);
          this.map.setMaxZoom(11);
          
          // 设置标志位
          this.isMapInitialized = true;
        }, 200);
      } catch (error) {
        console.error('创建地图时发生错误:', error);
        this.mapError = `创建地图时发生错误: ${error.message}`;
      }
    },

    // 超简化版的蓝色滤镜
    applySimpleOverlay() {
      // 使用最简单的蓝色半透明背景
      const mapEl = document.getElementById('osm-map');
      if (mapEl) {
        mapEl.style.backgroundColor = 'rgba(10, 41, 85, 0.3)';
        
        // 添加边缘填充元素确保没有空白区域
        const edgeFiller = document.createElement('div');
        edgeFiller.style.position = 'absolute';
        edgeFiller.style.top = '0';
        edgeFiller.style.left = '0';
        edgeFiller.style.right = '0';
        edgeFiller.style.bottom = '0';
        edgeFiller.style.backgroundColor = '#0a1525'; // 与容器背景色相同
        edgeFiller.style.zIndex = '0'; // 放在最底层
        mapEl.insertBefore(edgeFiller, mapEl.firstChild);
      }
    },
    
    // 使用节流函数优化resize事件
    handleResize: function() {
      if (!this.map) return;
      
      if (this.resizeTimer) {
        clearTimeout(this.resizeTimer);
      }
      
      this.resizeTimer = setTimeout(() => {
        this.map.invalidateSize();
      }, 200);
    }
  }
}
</script>

<style lang="scss" scoped>
.hangzhou-map {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  
  .map-container {
    width: 100%;
    height: 100%;
    background-color: #0a1525; // 深蓝色背景
    
    // 添加辉光效果
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: radial-gradient(circle at center, rgba(10, 70, 120, 0.3) 0%, rgba(10, 20, 40, 0.2) 80%, rgba(0, 0, 0, 0.3) 100%);
      pointer-events: none;
      z-index: 500;
    }
  }
  
  .map-error {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: rgba(255, 0, 0, 0.7);
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    z-index: 1000;
  }
  
  // 自定义Leaflet控件样式
  :deep(.leaflet-control-zoom) {
    border: none;
    box-shadow: 0 0 10px rgba(0, 149, 255, 0.3);
    
    a {
      background-color: rgba(10, 41, 85, 0.7) !important;
      color: #fff !important;
      border-color: rgba(0, 149, 255, 0.3) !important;
      
      &:hover {
        background-color: rgba(0, 100, 180, 0.7) !important;
      }
    }
  }
  
  :deep(.leaflet-control-scale) {
    border: none;
    
    .leaflet-control-scale-line {
      background-color: rgba(10, 41, 85, 0.7) !important;
      color: #fff !important;
      border-color: rgba(0, 149, 255, 0.3) !important;
    }
  }
  
  // 自定义地图属性控件样式
  :deep(.leaflet-control-attribution) {
    background-color: rgba(10, 41, 85, 0.7) !important;
    color: #fff !important;
    
    a {
      color: #4FC3F7 !important;
    }
  }
}
</style> 
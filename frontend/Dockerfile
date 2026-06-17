# ---- 构建阶段 ----
FROM node:20-alpine AS builder

WORKDIR /app

# 安装 pnpm 10（与本地及 lockfile 版本匹配）
RUN corepack enable && corepack prepare pnpm@10 --activate

# 先复制依赖清单，利用 Docker 缓存
COPY package.json pnpm-lock.yaml* ./

# 安装依赖（--ignore-scripts 跳过 pnpm 9 的构建审批，Vue/Vite 项目通常不需要 postinstall）
RUN pnpm install --frozen-lockfile --ignore-scripts

# 复制源码
COPY . .

# 构建（跳过 vue-tsc 类型检查，直接 vite build）
# 类型检查应在开发阶段或 CI 流程中完成
RUN pnpm exec vite build

# ---- 运行阶段 ----
FROM nginx:1.27-alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

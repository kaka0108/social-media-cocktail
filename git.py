# 1. 在GitHub创建新仓库，命名为 social-media-cocktails
# 2. 在本地打开命令提示符或Git Bash
cd "C:\Users\Lenovo\PycharmProjects\PythonProject"

# 3. 初始化git仓库
git init

# 4. 将文件添加到仓库
git add social_media_cocktails_with_images.html
# 如果还有CSS、JS、images文件夹，也要添加
git add .

# 5. 提交更改
git commit -m "Initial commit"

# 6. 连接到GitHub远程仓库
git branch -M main
git remote add origin https://github.com/你的用户名/social-media-cocktails.git
git push -u origin main
const { execSync } = require('child_process');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function exec(command) {
    console.log(`\n🔨 ${command}`);
    try {
        execSync(command, { stdio: 'inherit' });
        return true;
    } catch (error) {
        console.error(`❌ 失败: ${error.message}`);
        return false;
    }
}

rl.question('📦 请输入版本号 (如 v2.0.1): ', (version) => {
    if (!version.startsWith('v')) {
        console.error('❌ 版本号必须以 v 开头 (如 v2.0.1)');
        process.exit(1);
    }

    console.log(`\n🚀 开始发布 ${version}...\n`);

    // 1. 提交所有更改
    if (!exec('git add .')) process.exit(1);
    if (!exec(`git commit -m "Release ${version}"`)) {
        console.log('⚠️  没有新的更改需要提交');
    }

    // 2. 推送到 main
    if (!exec('git push origin main')) process.exit(1);

    // 3. 创建并推送标签
    if (!exec(`git tag -f ${version}`)) process.exit(1);
    if (!exec(`git push origin ${version} -f`)) process.exit(1);

    console.log('\n✅ 发布流程完成！');
    console.log(`\n👉 查看构建进度: https://github.com/jeneekuqtfbruckk-cyber/openwrt-manager/actions`);
    console.log(`👉 Release 页面: https://github.com/jeneekuqtfbruckk-cyber/openwrt-manager/releases\n`);

    rl.close();
});

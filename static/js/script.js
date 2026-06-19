document.addEventListener('DOMContentLoaded', function() {
    let myFunds = JSON.parse(localStorage.getItem('myFunds')) || [];
    let marketData = {};
    let pieChart = null;

    const CACHE_KEYS = {
        FUNDS: 'myFunds'
    };

    function parseNum(val, defaultVal = 0) {
        const parsed = parseFloat(val);
        return isNaN(parsed) ? defaultVal : parsed;
    }

    async function refresh() {
        if (myFunds.length === 0) {
            render();
            return;
        }

        const btn = document.getElementById('refresh-btn');
        if (btn) btn.innerText = "⏳ 同步中...";

        try {
            const codes = myFunds.map(f => f.code).join(',');
            const res = await fetch(`/api/fund/${codes}`);

            if (!res.ok) {
                throw new Error(`HTTP ${res.status}`);
            }

            const data = await res.json();
            data.forEach(item => {
                if (!item.error) marketData[item.code] = item;
            });

            render();
            updateDashboard();
        } catch (e) {
            console.error('Refresh failed:', e);
            alert('数据更新失败，请检查网络连接');
        } finally {
            if (btn) btn.innerText = "🔄 刷新";
        }
    }

    function render() {
        const tbody = document.getElementById('fund-list');
        tbody.innerHTML = '';

        myFunds.forEach((f, idx) => {
            const m = marketData[f.code] || {};
            const gsz = parseNum(m.gsz);
            const jz = parseNum(m.jz);
            const rate = parseNum(m.gszzl);
            const share = parseNum(f.share);
            const cost = parseNum(f.cost);

            const dayP = (gsz - jz) * share;
            const allP = (gsz - cost) * share;
            const isProfit = (val) => val >= 0;

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    <div class="fund-name">${m.name || '查询中...'}</div>
                    <div class="fund-code">${f.code}</div>
                </td>
                <td class="${isProfit(rate) ? 'red' : 'green'}">
                    ${gsz > 0 ? gsz.toFixed(4) : '--'}<br>
                    <small>${rate.toFixed(2)}%</small>
                </td>
                <td>
                    <div class="${isProfit(dayP) ? 'red' : 'green'}">今: ${dayP.toFixed(2)}</div>
                    <div class="${isProfit(allP) ? 'red' : 'green'}" style="opacity:0.6; font-size:0.8em">累: ${allP.toFixed(2)}</div>
                </td>
                <td><button onclick="removeF(${idx})" class="del-btn">×</button></td>
            `;
            tbody.appendChild(tr);
        });
    }

    function updateDashboard() {
        let tDay = 0, tAll = 0;

        myFunds.forEach(f => {
            const m = marketData[f.code];
            if (m) {
                const gsz = parseNum(m.gsz);
                const jz = parseNum(m.jz);
                const share = parseNum(f.share);
                const cost = parseNum(f.cost);

                if (gsz > 0) {
                    tDay += (gsz - jz) * share;
                    tAll += (gsz - cost) * share;
                }
            }
        });

        const formatProfit = (val) => (val >= 0 ? '+' : '') + val.toFixed(2);
        document.getElementById('day-profit').innerText = formatProfit(tDay);
        document.getElementById('total-profit').innerText = formatProfit(tAll);
    }

    document.getElementById('analyze-btn').onclick = async () => {
        const overlay = document.getElementById('loading-overlay');
        overlay.style.display = 'flex';

        let stockWeight = {};
        let totalVal = 0;
        let errorCount = 0;

        try {
            for (let f of myFunds) {
                const m = marketData[f.code];
                if (!m) continue;

                const gsz = parseNum(m.gsz);
                if (gsz <= 0) continue;

                const share = parseNum(f.share);
                const val = share * gsz;
                totalVal += val;

                try {
                    const res = await fetch(`/api/stocks/${f.code}`);
                    if (!res.ok) continue;

                    const stocks = await res.json();
                    stocks.forEach(s => {
                        const rate = parseNum(s.rate, 0);
                        const amt = val * (rate / 100);
                        stockWeight[s.name] = (stockWeight[s.name] || 0) + amt;
                    });
                } catch (e) {
                    errorCount++;
                    console.error(`Failed to fetch stocks for ${f.code}:`, e);
                }
            }

            if (totalVal === 0) {
                alert("请先刷新行情");
                return;
            }

            const data = Object.entries(stockWeight)
                .map(([name, amt]) => ({ name, val: ((amt / totalVal) * 100).toFixed(2) }))
                .sort((a, b) => b.val - a.val)
                .slice(0, 10);

            if (data.length > 0) {
                document.getElementById('analysis-panel').style.display = 'block';
                if (pieChart) pieChart.destroy();

                pieChart = new Chart(document.getElementById('stockPieChart'), {
                    type: 'doughnut',
                    data: {
                        labels: data.map(d => d.name),
                        datasets: [{
                            data: data.map(d => d.val),
                            backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#14b8a6', '#f97316', '#6366f1']
                        }]
                    },
                    options: { cutout: '70%' }
                });

                if (errorCount > 0) {
                    console.warn(`${errorCount} fund(s) failed to load`);
                }
            } else {
                alert("接口暂被拦截，已启用本地缓存保护，请1分钟后重试。");
            }
        } finally {
            overlay.style.display = 'none';
        }
    };

    window.removeF = (i) => {
        myFunds.splice(i, 1);
        localStorage.setItem(CACHE_KEYS.FUNDS, JSON.stringify(myFunds));
        refresh();
    };

    document.getElementById('add-btn').onclick = () => {
        document.getElementById('addModal').style.display = 'flex';
    };

    document.getElementById('modal-cancel').onclick = () => {
        document.getElementById('addModal').style.display = 'none';
    };

    document.getElementById('modal-save').onclick = () => {
        const code = document.getElementById('inp-code').value.trim();
        const share = document.getElementById('inp-share').value.trim();
        const cost = document.getElementById('inp-cost').value.trim();

        if (!code || !share) {
            alert('请填写基金代码和份额');
            return;
        }

        if (!/^\d{6}$/.test(code)) {
            alert('基金代码应为6位数字');
            return;
        }

        const shareVal = parseNum(share);
        const costVal = parseNum(cost);

        if (shareVal <= 0) {
            alert('份额必须大于0');
            return;
        }

        myFunds.push({ code, share: shareVal, cost: costVal || 0 });
        localStorage.setItem(CACHE_KEYS.FUNDS, JSON.stringify(myFunds));
        document.getElementById('addModal').style.display = 'none';

        document.getElementById('inp-code').value = '';
        document.getElementById('inp-share').value = '';
        document.getElementById('inp-cost').value = '';

        refresh();
    };

    document.getElementById('refresh-btn').onclick = refresh;
    refresh();
});
// Git履歴から作成日時を取得する。ブラウザーでは履歴APIを呼ばない。
const fs=require('node:fs'),path=require('node:path'),{execFileSync}=require('node:child_process');
const root=path.resolve(__dirname,'..');
const articles=fs.readdirSync(path.join(root,'notes'),{withFileTypes:true}).filter(d=>d.isDirectory()).flatMap(d=>{
 const file=`notes/${d.name}/article.md`;
 if(!fs.existsSync(path.join(root,file)))return [];
 const dates=execFileSync('git',['log','--format=%cI','--',file],{cwd:root,encoding:'utf8'}).trim().split(/\r?\n/).filter(Boolean);
 if(!dates.length)throw Error('Missing Git history: '+file);
 return [{key:d.name,created:dates.at(-1),text:fs.readFileSync(path.join(root,file),'utf8')}];
}).sort((a,b)=>Date.parse(b.created)-Date.parse(a.created)||a.key.localeCompare(b.key));
fs.writeFileSync(path.join(root,'notes/catalog.json'),JSON.stringify({schemaVersion:1,articles},null,2)+'\n');
console.log(`Catalog: ${articles.length} articles`);

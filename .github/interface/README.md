# Cliente RustDesk da Interface Sistemas

Fork do `rustdesk/rustdesk` com build próprio do cliente Windows, já com a marca e o servidor
`rustdesk.interfacesistemas.com` embutidos. O usuário abre o programa e ele já conecta, sem
configurar ⋮ → Rede.

- Workflow: `.github/workflows/interface-windows.yml` (disparo manual, Windows x64).
- Marca: `.github/interface/apply_branding.py` + `assets/` (logo, ícone, laranja `#F04E23`).
  Só roda no CI; o código do upstream não é alterado no repo, o que facilita atualizar o fork.
- Saída: `InterfaceSuporte.exe` (portátil; dá para instalar como serviço pelo próprio app), enviado
  por sftp para a VPS. Download só logado, em `https://licencas.interfacesistemas.com/suporte-remoto`
  (com instruções). Não fica como artefato no GitHub.

## Secrets / variables (Settings → Secrets and variables → Actions)

| Nome | Tipo | Valor |
|---|---|---|
| `RS_HOST` | secret | `rustdesk.interfacesistemas.com` |
| `RS_PUB_KEY` | secret | chave pública do servidor (a mesma dos clientes de hoje) |
| `VPS_HOST` | secret | IP da VPS (impresso pelo `setup-rdupload.sh`) |
| `VPS_PORT` | secret | só se o SSH não for a porta 22 |
| `VPS_KNOWN_HOSTS` | secret | linhas do `ssh-keyscan` impressas pelo `setup-rdupload.sh` |
| `VPS_UPLOAD_KEY` | secret | chave privada do usuário `rdupload` (`/root/interface-rdupload/id_ed25519`) |
| `APP_NAME` | variable (opcional) | nome do app/serviço, sem espaços; padrão `InterfaceSuporte` |

O lado da VPS fica em `interfacesistemas/sisposto-licencas` (`infra/setup-rdupload.sh`, tela Suporte remoto).

## Atualizar para uma versão nova do RustDesk

GitHub → **Sync fork** → rodar o workflow de novo. Se o build falhar depois do sync, comparar os
passos com o job `build-for-windows-flutter` (x86_64) de `flutter-build.yml`.

## Avisos conhecidos

- Sem assinatura de código: o Windows (SmartScreen) avisa uma vez por arquivo baixado.
- Licença AGPL-3.0: este fork é público, o que cumpre a obrigação de oferecer o código-fonte.

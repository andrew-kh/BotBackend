# BotBackend
pymongo scripts


# run script regularly from Mac Os terminal:

1. in script, set 1st line to: #!/Users/andrew/anaconda3/bin/python (path to python user's python bin)
2. in terminal, change access rights of script: chmod a+x /Users/andrew/.../script.py
3. in terminal, run `env EDITOR=nano crontab -e` (vi used to throw errors...)
4. in crontab, insert rule: `*/3 * * * * /Users/andrew/PycharmProjects/Proj/script.py`
5. press `ctrl+O` then `ENTER` then `ctrl+X`
  
Now script.py will be executed every 3rd minute

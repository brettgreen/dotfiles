#!/bin/bash
#
# Creates 3 drafts in Apple Mail. Nothing is sent.
#
# Run it with:   bash create_drafts.sh
#
# The first time, macOS asks whether Terminal may control Mail. Click OK.
#
# Drafts are created from the account below. If they come out from the
# wrong address, change it to match the account exactly as it appears in
# Mail > Settings > Accounts, then run this again.

SENDER="b.green@wustl.edu"

echo "Creating 3 draft(s) in Apple Mail..."

echo "  [1/3] Committee feedback on Ethics and Responsible AI"
read -r -d '' SUBJECT_1 <<'SUBJECT_END' || true
Committee feedback on Ethics and Responsible AI
SUBJECT_END

read -r -d '' BODY_1 <<'BODY_END' || true
Dear Gerald,

The committee reviewed your proposal and it received the strongest support of the five. I'm moving it to an email vote.

One note: several members suggested a foundational AI course as a prerequisite. It's a suggestion, not a condition.

Best,
Brett
BODY_END

osascript - "$SUBJECT_1" "$BODY_1" "$SENDER" <<'APPLESCRIPT'
on run argv
    set theSubject to item 1 of argv
    set theBody to item 2 of argv
    set theSender to item 3 of argv
    tell application "Mail"
        set msg to make new outgoing message with properties {subject:theSubject, content:theBody, visible:false}
        if theSender is not "" then
            try
                tell msg to set sender to theSender
            on error
                log "  note: sender " & theSender & " did not match a Mail account; the default account was used instead."
            end try
        end if
        tell msg
            -- no recipients: add them in Mail before sending
        end tell
        save msg
    end tell
end run
APPLESCRIPT

echo "  [2/3] Committee feedback on Business of Health Technology"
read -r -d '' SUBJECT_2 <<'SUBJECT_END' || true
Committee feedback on Business of Health Technology
SUBJECT_END

read -r -d '' BODY_2 <<'BODY_END' || true
Dear Patrick,

The committee would like to invite you to revise and resubmit. The main concerns were positioning relative to Health Analytics, and the fact that the syllabus mentions quizzes that don't appear in the grading rubric.

Best,
Brett
BODY_END

osascript - "$SUBJECT_2" "$BODY_2" "$SENDER" <<'APPLESCRIPT'
on run argv
    set theSubject to item 1 of argv
    set theBody to item 2 of argv
    set theSender to item 3 of argv
    tell application "Mail"
        set msg to make new outgoing message with properties {subject:theSubject, content:theBody, visible:false}
        if theSender is not "" then
            try
                tell msg to set sender to theSender
            on error
                log "  note: sender " & theSender & " did not match a Mail account; the default account was used instead."
            end try
        end if
        tell msg
            -- no recipients: add them in Mail before sending
        end tell
        save msg
    end tell
end run
APPLESCRIPT

echo "  [3/3] Committee feedback on DAT 5565 and DAT 5668"
read -r -d '' SUBJECT_3 <<'SUBJECT_END' || true
Committee feedback on DAT 5565 and DAT 5668
SUBJECT_END

read -r -d '' BODY_3 <<'BODY_END' || true
Dear Salih,

The committee is returning both proposals for revision. The prerequisites don't agree across documents, and DAT 5668 can't advance ahead of DAT 5565.

Best,
Brett
BODY_END

osascript - "$SUBJECT_3" "$BODY_3" "$SENDER" <<'APPLESCRIPT'
on run argv
    set theSubject to item 1 of argv
    set theBody to item 2 of argv
    set theSender to item 3 of argv
    tell application "Mail"
        set msg to make new outgoing message with properties {subject:theSubject, content:theBody, visible:false}
        if theSender is not "" then
            try
                tell msg to set sender to theSender
            on error
                log "  note: sender " & theSender & " did not match a Mail account; the default account was used instead."
            end try
        end if
        tell msg
            -- no recipients: add them in Mail before sending
        end tell
        save msg
    end tell
end run
APPLESCRIPT

echo ""
echo "Done. Check your Drafts folder. 3 draft(s) have no recipient yet — add them before sending."
